from flask import Flask, request, render_template, url_for

from time import sleep

import subprocess

import numpy as np

import os
import boto3
import datetime
from dotenv import load_dotenv
import pandas as pd
import awswrangler as wr


load_dotenv()

s3 = boto3.resource(
    service_name="s3",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
)

# from ETL.WeatherKafkaProducer import kafkaProducer
# from ETL.WeatherKafkaConsumer import kafkaConsumer

app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/userSubmitCities", methods=["POST"])
def userSubmitCities():


        print("Server: userSubmitCities executed")
        get_last_modified = lambda obj: int(obj["LastModified"].strftime("%s"))

        s3 = boto3.client("s3")
        objs = s3.list_objects_v2(Bucket="weatherdata-project")["Contents"]
        last_added = [
            obj["Key"] for obj in sorted(objs, key=get_last_modified, reverse=True)
        ][0]
        print(f"last_added: {last_added}")
        df = wr.s3.read_csv(f"s3://weatherdata-project/{last_added}")
        df.drop(columns=["Unnamed: 0", "TimeZone"], inplace=True)
        arrayOfRows = []
        for index, row in df.iterrows():
            arrayOfRows.append(row.values)

        listOfData = [arr.tolist() for arr in arrayOfRows]
        return render_template("home.html", status=True, dataframe=df, data=listOfData)


# @app.route("weather")
# def weatherDataSchedular():
#     get_last_modified = lambda obj: int(obj["LastModified"].strftime("%s"))

#     s3 = boto3.client("s3")
#     objs = s3.list_objects_v2(Bucket="weatherdata-project")["Contents"]
#     last_added = [
#         obj["Key"] for obj in sorted(objs, key=get_last_modified, reverse=True)
#     ][0]
#     print(f"last_added: {last_added}")
#     df = wr.s3.read_csv(f"s3://weatherdata-project/{last_added}")
#     df.drop(columns=["Unnamed: 0", "TimeZone"], inplace=True)
#     arrayOfRows = []
#     for index, row in df.iterrows():
#         arrayOfRows.append(row.values)

#     listOfData = [arr.tolist() for arr in arrayOfRows]
#     return render_template("home.html", status=True, dataframe=df, data=listOfData)


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
