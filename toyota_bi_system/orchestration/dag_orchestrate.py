from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Tambahkan path root project agar bisa import modul monitoring
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modul Alerting dan Backup
from monitoring.alerts import send_error_email
from monitoring.backup_manager import BackupManager

def run_backup_task():
    """Execute backup procedure using BackupManager"""
    manager = BackupManager()
    manager.perform_full_backup()

default_args = {
    'owner': 'rifky',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1, 
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': send_error_email
}

with DAG(
    dag_id='toyota_master_orchestration',
    default_args=default_args,
    description='Master DAG with Disaster Recovery Plan (Alerts & Backup)',
    schedule_interval='@weekly',
    catchup=False,
    tags=['orchestration', 'master', 'toyota']
) as dag:
    
    start = DummyOperator(task_id='start_pipeline')
    
    # 1. Trigger Ingestion Layer
    trigger_ingestion = TriggerDagRunOperator(
        task_id='trigger_data_ingestion',
        trigger_dag_id='toyota_data_ingestion',
        wait_for_completion=True,
        poke_interval=30,
        reset_dag_run=True
    )
    
    # 2. Trigger Transformation Layer (ETL)
    trigger_transform = TriggerDagRunOperator(
        task_id='trigger_etl_transform',
        trigger_dag_id='toyota_etl_transform',
        wait_for_completion=True,
        poke_interval=30,
        reset_dag_run=True
    )
    
    # 3. Trigger Data Warehouse Load Layer
    trigger_dwh = TriggerDagRunOperator(
        task_id='trigger_dwh_load',
        trigger_dag_id='toyota_load_dwh',
        wait_for_completion=True,
        poke_interval=30,
        reset_dag_run=True
    )
    
    # 4. Trigger Machine Learning Pipeline
    trigger_ml = TriggerDagRunOperator(
        task_id='trigger_ml_pipeline',
        trigger_dag_id='toyota_ml_pipeline',
        wait_for_completion=True,
        poke_interval=30,
        reset_dag_run=True
    )
    
    # 5. AUTO BACKUP (Disaster Recovery Checkpoint)
    # Task ini hanya jalan jika pipeline ML sukses
    backup_data = PythonOperator(
        task_id='perform_auto_backup',
        python_callable=run_backup_task
    )
    
    end = DummyOperator(task_id='pipeline_complete')
    
    # Define Workflow: Ingest -> Transform -> DWH -> ML -> Backup
    start >> trigger_ingestion >> trigger_transform >> trigger_dwh >> trigger_ml >> backup_data >> end