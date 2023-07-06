import boto3
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.resource(
    service_name="s3",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
)

currentPath = os.getcwd()


def loadData(df):

    files = os.listdir(currentPath)
    for file in files:
        if file.startswith("weather") and file.endswith(".csv"):
            os.remove(f"{currentPath}/{file}")

    now = datetime.datetime.now()
    df.to_csv("weatherData_at_{}.csv".format(now))
    print(df)
    s3.Bucket("weatherdata-project").upload_file(
        Filename="weatherData_at_{}.csv".format(now),
        Key="weatherData_s3_at_{}.csv".format(now),
    )
