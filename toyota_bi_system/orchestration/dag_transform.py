from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dwh.etl_transform import ETLTransformer

default_args = {
    'owner': 'rifky',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

def run_etl_transform():
    """Run ETL transformation"""
    print("Starting ETL transformation...")
    transformer = ETLTransformer()
    result = transformer.run_transform()
    return result is not None

with DAG(
    dag_id='toyota_etl_transform',
    default_args=default_args,
    description='Transform raw data into processed format',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'transform', 'toyota']
) as dag:
    
    start = DummyOperator(task_id='start')
    
    transform_data = PythonOperator(
        task_id='run_etl_transformation',
        python_callable=run_etl_transform,
        provide_context=True
    )
    
    end = DummyOperator(task_id='end')
    
    start >> transform_data >> end