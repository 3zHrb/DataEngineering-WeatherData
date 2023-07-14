from kafka import KafkaProducer
import time
import weatherAPI


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: str(x).encode("utf-8"),
)

arrayOfCities = ["Jeddah", "Riyadh", "San Francisco", "Los Angeles", "Dubai"]


def kafkaProducer():
    while True:
        producer.send("weatherData", weatherAPI.weatherDataRequest(arrayOfCities))
        time.sleep(3)


kafkaProducer()
