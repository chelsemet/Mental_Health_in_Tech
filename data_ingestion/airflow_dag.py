from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import bigquery
from datetime import datetime
import pandas as pd


from data_cleaning import data_cleaning
from data_transformation import covariance

DATA_DIR = '/opt/airflow/data'

def clean(**kwargs):
    df = pd.read_csv(f'{DATA_DIR}/survey.csv')
    df = data_cleaning(df)
    df.to_csv(f'{DATA_DIR}/clean.csv', index=False)

def transform(**kwargs):
    df = pd.read_csv(f'{DATA_DIR}/clean.csv')
    cov_df = covariance(df)
    cov_df.to_csv(f'{DATA_DIR}/covariance.csv', index=False)

def validate(**kwargs):
    df = pd.read_csv(f'{DATA_DIR}/clean.csv')
    if df.empty:
        raise ValueError("Data validation failed: Empty file")
    cov_df = pd.read_csv(f'{DATA_DIR}/covariance.csv')
    if cov_df.empty:
        raise ValueError("Data validation failed: Empty file")

def upload(**kwargs):
    # Example DataFrame
    df = pd.read_csv(f'{DATA_DIR}/clean.csv')
    cov_df = pd.read_csv(f'{DATA_DIR}/covariance.csv')

    # Initialize client
    client = bigquery.Client()

    # Set your table ID: 'project.dataset.table'
    table_id = "kestra-sandbox-450921.mental_health_survey.clean_data"

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        time_partitioning=None,
        range_partitioning=bigquery.RangePartitioning(
            field="Age",
            range_=bigquery.PartitionRange(start=0, end=100, interval=10)
        ),
        clustering_fields=["Country", "tech_company", "gender_clean"]
    )
    
    # Upload DataFrame
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Wait for the job to complete
    job.result()
    print("Data uploaded to BigQuery successfully:", table_id)

    job_config = bigquery.LoadJobConfig(
        autodetect=True
    )

    table_id = "kestra-sandbox-450921.mental_health_survey.covariance"

    job = client.load_table_from_dataframe(cov_df, table_id, job_config=job_config)
    
    job.result()
    print("Data uploaded to BigQuery successfully:", table_id)

with DAG('e2e_pipeline',
         description='Extract, transform, validate, and upload mental health survey data',
         default_args={'owner': 'airflow'},
         start_date=datetime(2025, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    t1 = PythonOperator(task_id='clean', python_callable=clean)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='validate', python_callable=validate)
    t4 = PythonOperator(task_id='upload', python_callable=upload)

    t1 >> t2 >> t3 >> t4
