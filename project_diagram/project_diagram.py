from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.aws import storage

openWeather_icon = "/Users/abdulazizalharbi/Desktop/Old-Desktop/Data_Engineering/WeatherData/OPENWEATHER.png"
kafka_icon = (
    "/Users/abdulazizalharbi/Desktop/Old-Desktop/Data_Engineering/WeatherData/kafka.png"
)

pandas_icon = "/Users/abdulazizalharbi/Desktop/Old-Desktop/Data_Engineering/WeatherData/Pandas_logo.svg.png"
website_icon = "/Users/abdulazizalharbi/Desktop/Old-Desktop/Data_Engineering/WeatherData/website.png"
with Diagram("Weather Data", direction="LR"):
    with Cluster(
        "Extraction",
        direction="TB",
        graph_attr={"style": "rounded", "bgcolor": "lightblue", "fontsize": "12"},
    ):
        openWeatherAPI = Custom(
            "OpenWeatherAPI",
            openWeather_icon,
        )
        kafkaProducer = Custom(
            "Kafka Producer",
            kafka_icon,
        )
        kafkaTopic = Custom(
            "Kafka Topic",
            kafka_icon,
        )
        extraction = openWeatherAPI >> kafkaProducer >> kafkaTopic
    with Cluster(
        "Transform & Load",
        graph_attr={"style": "rounded", "bgcolor": "lightyellow", "fontsize": "12"},
    ):
        kafkaConsumer = Custom("Kafka Consumer", kafka_icon)
        transform = Custom("Pandas", pandas_icon)
        load = storage.S3("AWS S3")
        transformationAndLoading = kafkaConsumer >> transform >> load
    with Cluster("Website", graph_attr={"style": "rounded"}):
        website = Custom("Website", website_icon)

    extraction >> transformationAndLoading
    transformationAndLoading >> website

    # extraction >> transformationAndLoading >> website
