from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests

default_args={
    'owner':'Arun',
    'start_date':datetime(2025,2,25,10,00,00)
}

def stream_data():
    res= requests.get("https://randomuser.me/api/")
    print(res.json())

# with DAG('user_automation',
#           default_args=default_args,
#           schedule='@daily',
#           catchup=False) as dag:
#
#     streaming_task=PythonOperator(task_id='stream_data_from_API',
#                                   python_callable=stream_data
#                                   )

stream_data()