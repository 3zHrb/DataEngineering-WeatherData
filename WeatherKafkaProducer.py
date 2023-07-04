from kafka import KafkaProducer
import time
import weatherAPI
import json


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    # value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    value_serializer=lambda x: str(x).encode("utf-8"),
)

arrayOfCities = ["Boston", "Tokyo"]

while True:

    # for city in arrayOfCities:

    producer.send("weatherData", weatherAPI.weatherDataRequest(arrayOfCities))

    time.sleep(3)
