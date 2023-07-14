from kafka import KafkaConsumer
from transform import transformData
import load
import requests

# import website.server as server


def kafkaConsumer():

    consumerData = KafkaConsumer(
        "weatherData",
        bootstrap_servers="localhost:9092",
    )
    for index, messages in enumerate(consumerData):
        df = transformData(messages=messages)
        s3FileName = load.loadData(df)


kafkaConsumer()
