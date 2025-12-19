from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os

# --- HAPUS IMPORT DARI ATAS SINI ---
# Jangan import file 'ml' di level atas agar DAG tidak Broken saat parsing.

def run_feature_engineering():
    """Run feature engineering and save to disk"""
    print("Starting feature engineering...")
    
    # --- PINDAHKAN IMPORT KE DALAM FUNGSI (LAZY IMPORT) ---
    # Tambahkan path manual untuk memastikan docker mengenali folder root
    import sys
    sys.path.append('/opt/airflow') 
    
    from ml.feature_engineering import main as feature_eng_main
    
    result = feature_eng_main()
    return result

def run_model_training():
    """Run model training loading from disk"""
    print("Starting model training...")
    
    # --- PINDAHKAN IMPORT KE DALAM FUNGSI ---
    import sys
    sys.path.append('/opt/airflow')
    
    from ml.train_model import main as train_model_main
    
    train_model_main()
    return "Training Complete"

default_args = {
    'owner': 'rifky',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    dag_id='toyota_ml_pipeline',
    default_args=default_args,
    description='Machine Learning pipeline for price prediction',
    schedule_interval='@weekly',
    catchup=False,
    tags=['ml', 'machinelearning', 'toyota']
) as dag:
    
    start = DummyOperator(task_id='start')
    
    feature_eng = PythonOperator(
        task_id='run_feature_engineering',
        python_callable=run_feature_engineering
    )
    
    model_train = PythonOperator(
        task_id='run_model_training',
        python_callable=run_model_training
    )
    
    end = DummyOperator(task_id='end')
    
    start >> feature_eng >> model_train >> end