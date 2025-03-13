FROM apache/airflow:2.0.0
COPY requirements.txt .
RUN pip install -r requirements.txt