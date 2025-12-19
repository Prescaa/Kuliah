from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dwh.load_dimensions import DimensionLoader
from dwh.load_facts import FactLoader

default_args = {
    'owner': 'rifky',
    'depends_on_past': True,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
}

def load_dimensions():
    """Load dimension tables"""
    print("Loading dimension tables...")
    loader = DimensionLoader()
    success = loader.load_all_dimensions()
    return success

def load_facts():
    """Load fact tables"""
    print("Loading fact tables...")
    loader = FactLoader()
    success = loader.load_all_facts()
    return success

with DAG(
    dag_id='toyota_load_dwh',
    default_args=default_args,
    description='Load data into Data Warehouse',
    schedule_interval='@daily',
    catchup=False,
    tags=['dwh', 'datawarehouse', 'toyota']
) as dag:
    
    start = DummyOperator(task_id='start')
    
    load_dim = PythonOperator(
        task_id='load_dimension_tables',
        python_callable=load_dimensions,
        provide_context=True
    )
    
    load_fact = PythonOperator(
        task_id='load_fact_tables',
        python_callable=load_facts,
        provide_context=True
    )
    
    end = DummyOperator(task_id='end')
    
    start >> load_dim >> load_fact >> end