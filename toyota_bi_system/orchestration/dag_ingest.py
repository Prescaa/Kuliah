from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingest.ingest_csv_batch import CSVIngestor
from ingest.ingest_api_nhtsa import NHTSAIngestor

default_args = {
    'owner': 'rifky',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

def ingest_csv_data():
    """Task to ingest CSV data"""
    print("Starting CSV ingestion...")
    ingestor = CSVIngestor()
    results = ingestor.ingest_all()
    return results

def ingest_api_data():
    """Task to ingest API data"""
    print("Starting API ingestion...")
    ingestor = NHTSAIngestor(use_mock=True)  # Use mock for testing
    
    # Create sample vehicle data
    import pandas as pd
    sample_vehicles = pd.DataFrame([
        {'make': 'Toyota', 'model': 'CAMRY', 'year': 2020},
        {'make': 'Toyota', 'model': 'COROLLA', 'year': 2021},
        {'make': 'Toyota', 'model': 'RAV4', 'year': 2022},
        {'make': 'Toyota', 'model': 'HIGHLANDER', 'year': 2021},
        {'make': 'Toyota', 'model': 'TACOMA', 'year': 2020}
    ])
    
    results = ingestor.process_vehicle_list(sample_vehicles)
    return results is not None

with DAG(
    dag_id='toyota_data_ingestion',
    default_args=default_args,
    description='Ingest data from CSV files and APIs',
    schedule_interval='@daily',
    catchup=False,
    tags=['ingestion', 'toyota']
) as dag:
    
    start = DummyOperator(task_id='start')
    
    ingest_csv = PythonOperator(
        task_id='ingest_csv_data',
        python_callable=ingest_csv_data,
        provide_context=True
    )
    
    ingest_api = PythonOperator(
        task_id='ingest_api_data',
        python_callable=ingest_api_data,
        provide_context=True
    )
    
    end = DummyOperator(task_id='end')
    
    start >> [ingest_csv, ingest_api] >> end