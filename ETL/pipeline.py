from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import WeatherKafkaProducer
import WeatherKafkaConsumer


dag = DAG(
    dag_id="WeatherData Pipeline", schedule="@daily", start_date=datetime(2023, 7, 6)
)

kafkaProducer_task = PythonOperator(
    task_id="Kafka Producer",
    python_callable=WeatherKafkaProducer.kafkaProducer,
    dag=dag,
)

kafkaConsumer_task = PythonOperator(
    task_id="Kafka Consumer",
    python_callable=WeatherKafkaConsumer.kafkaConsumer,
    dag=dag,
)

kafkaProducer_task >> kafkaConsumer_task
