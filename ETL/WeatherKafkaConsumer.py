from kafka import KafkaConsumer
from transform import transformData
import load


def kafkaConsumer():

    consumerData = KafkaConsumer(
        "weatherData",
        bootstrap_servers="localhost:9092",
    )
    for index, messages in enumerate(consumerData):
        df = transformData(messages=messages)
        load.loadData(df)


kafkaConsumer()
