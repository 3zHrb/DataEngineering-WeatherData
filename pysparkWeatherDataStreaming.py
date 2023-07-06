## Note this file is not used in the project

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import findspark
import ast
from kafka import KafkaConsumer
from json import loads

import os
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()


SPARK_VERSION = "3.1.2"

SCALA_VERSION = "2.12"


findspark.add_packages(
    ["org.apache.spark:spark-sql-kafka-0-10_" + SCALA_VERSION + ":" + SPARK_VERSION]
)
findspark.init()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("aws_access_key_id")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("aws_secret_access_key")

print(os.environ["AWS_ACCESS_KEY_ID"])
print(os.environ["AWS_SECRET_ACCESS_KEY"])


import pyspark.sql.functions as F
import pyspark.sql.types as T

# schema = StructType(
#     [
#         StructField("name", StringType()),
#         StructField("temp", DoubleType()),
#         StructField("timezone", IntegerType()),
#     ]
# )

schema = T.ArrayType(T.StringType(), containsNull=False)


def parse_array_str(arr_str):
    return ast.literal_eval(arr_str)


sc = SparkContext()


sparkSession = SparkSession(sc).builder.appName("weatherData").getOrCreate()

hadoopConf = sc._jsc.hadoopConfiguration()
hadoopConf.set("fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"])
hadoopConf.set("fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"])
hadoopConf.set(
    "spark.hadoop.fs.s3a.aws.credentials.provider",
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
)

df = (
    sparkSession.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "weatherData")
    .option("startingOffsets", "latest")
    .load()
    .select("value")
    .selectExpr("CAST(value AS STRING)")
    .withColumn("array_data", F.from_json(F.col("value"), schema))
    .select(F.explode("array_data").alias("col"))
    .withColumn("col_array", F.split("col", ","))
    .withColumn("city", F.col("col_array").getItem(0))
    .withColumn("timezone", F.col("col_array").getItem(2))
    .withColumn("city", F.regexp_replace("city", "[\\['\"]", "").cast("string"))
    .withColumn("temp", F.col("col_array").getItem(1).cast("float"))
    .withColumn("timezone", F.regexp_replace("timezone", "[\\]'\"]", "").cast("int"))
    .drop("value")
    .drop("col")
    .drop("col_array")
)


print(df.printSchema())


# streaming = (
#     df.writeStream.format("console")
#     # .trigger(processingTime="1 seconds")
#     .outputMode("append").start()
# )

# streaming.awaitTermination()


# pandas_df = df.collect()
# print(pandas_df.show())

currentPath = os.getcwd()


query = (
    df.writeStream.format("csv")
    # .option("checkpointLocation", f"{currentPath}/dataframeTermpraryHolder")
    .option("path", "s3a://weatherdata-project/your_prefix").start()
)
# query.awaitTermination()
