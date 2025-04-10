from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import bigquery
from datetime import datetime
import pandas as pd

DATA_DIR = '/opt/airflow/data'

def transform(**kwargs):
    df = pd.read_csv(f'{DATA_DIR}/survey.csv')
    df.dropna(inplace=True)
    df.to_csv(f'{DATA_DIR}/clean.csv', index=False)

def validate(**kwargs):
    df = pd.read_csv(f'{DATA_DIR}/clean.csv')
    if df.empty:
        raise ValueError("Data validation failed: Empty file")

def upload(**kwargs):
    # Example DataFrame
    df = pd.read_csv(f'{DATA_DIR}/clean.csv')

    # Initialize client
    client = bigquery.Client()

    # Set your table ID: 'project.dataset.table'
    table_id = "kestra-sandbox-450921.mental_health_survey.clean_data"

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
    )
    
    # Upload DataFrame
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Wait for the job to complete
    job.result()
    print("Data uploaded to BigQuery successfully:", table_id)

with DAG('e2e_pipeline',
         description='Extract, transform, validate, and upload mental health survey data',
         default_args={'owner': 'airflow'},
         start_date=datetime(2025, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    t1 = PythonOperator(task_id='transform', python_callable=transform)
    t2 = PythonOperator(task_id='validate', python_callable=validate)
    t3 = PythonOperator(task_id='upload', python_callable=upload)

    t1 >> t2 >> t3
