from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests
from kafka import KafkaProducer, KafkaConsumer
import time
from pyarrow.compute import index

default_args={
    'owner':'Arun',
    'start_date':datetime(2025,2,25,10,00,00)
}

def get_data():
    res= requests.get("https://randomuser.me/api/")
    res=res.json()
    res=res['results'][0]
    return res

def format_data(res):
    data={}
    data['first_name']=res['name']['first']
    data['last_name']=res['name']['last']
    data['gender']=res['gender']
    data['address']=str(res['location']['street']['number']) + ' ' + res['location']['street']['name'] + ' ' + res['location']['city'] + ' ' + res['location']['state'] + ' ' + res['location']['country']
    data['postcode']=res['location']['postcode']
    data['email']=res['email']
    data['username']=res['login']['username']
    data['dob']=res['dob']['date']
    data['registered_date']=res['registered']['date']
    data['phone']=res['phone']
    data['picture']=res['picture']['medium']

    return data

def stream_data():
    res=get_data()
    res=format_data(res)
    print(json.dumps(res, indent=3))
    producer=KafkaProducer(bootstrap_servers=['localhost:9092'],max_block_ms=5000)
    producer.send('users_created', json.dumps(res).encode('utf-8'))

# with dags('user_automation',
#           default_args=default_args,
#           schedule='@daily',
#           catchup=False) as dag:
#
#     streaming_task=PythonOperator(task_id='stream_data_from_API',
#                                   python_callable=stream_data
#                                   )

stream_data()