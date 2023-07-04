from kafka import KafkaConsumer
import json
import boto3
import ast
import pandas as pd
import datetime
import os

from dotenv import load_dotenv

load_dotenv()


consumer = KafkaConsumer(
    "weatherData",
    bootstrap_servers="localhost:9092",
    # value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)
# s3 = S3FileSystem()

s3 = boto3.resource(
    service_name="s3",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
)


print("the project has started ...")

currentPath = os.getcwd()


for index, messages in enumerate(consumer):
    files = os.listdir(currentPath)
    for file in files:
        if file.startswith("weather") and file.endswith(".csv"):
            os.remove(f"{currentPath}/{file}")

    messageValuetoArray = ast.literal_eval(messages.value.decode())
    print(messageValuetoArray)
    print(type(messageValuetoArray))
    print(messageValuetoArray[0][0])
    df = pd.DataFrame(
        {
            "CityName": [messageValuetoArray[0][0], messageValuetoArray[1][0]],
            "Temperature": [messageValuetoArray[0][1], messageValuetoArray[1][1]],
            "TimeZone": [messageValuetoArray[0][2], messageValuetoArray[1][2]],
        }
    )
    now = datetime.datetime.now()
    df.to_csv("weatherData_at_{}.csv".format(now))

    s3.Bucket("weatherdata-project").upload_file(
        Filename="weatherData_at_{}.csv".format(now),
        Key="weatherData_s3_at_{}.csv".format(now),
    )
