import requests
import os
import json
from datetime import datetime

def send_error_email(context):
    """
    Function to be called when a DAG/Task fails.
    Sends SMART ALERT notification to Discord Webhook.
    """
    # 1. Ambil Webhook URL dari Docker Environment
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    if not webhook_url:
        print("[WARNING] Discord Webhook URL not found. Skipping alert.")
        return

    # 2. Ambil detail error dari context Airflow
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    log_url = task_instance.log_url
    execution_date = context.get('execution_date')
    exception = context.get('exception')

    # -------------------------------------------------------------
    # 3. DIAGNOSIS OTOMATIS (Smart Analysis)
    # Kita terjemahkan Task ID menjadi pesan error yang manusiawi
    # -------------------------------------------------------------
    diagnosis = "Penyebab spesifik tidak diketahui. Cek log untuk detail."
    possible_fix = "Cek Log Airflow."

    if task_id == 'trigger_etl_transform':
        diagnosis = "CRITICAL: Proses Transformasi Data Gagal."
        possible_fix = "1. Cek apakah file CSV Raw ada di folder data/enterprise_raw.\n2. Cek apakah format kolom CSV berubah."
    
    elif task_id == 'trigger_data_ingestion':
        diagnosis = "WARNING: Gagal mengambil data mentah."
        possible_fix = "1. Cek koneksi internet (API NHTSA).\n2. Cek folder data/raw apakah file sumber tersedia."
        
    elif task_id == 'trigger_dwh_load':
        diagnosis = "CRITICAL: Gagal mengisi Data Warehouse."
        possible_fix = "1. Cek apakah container Database (Postgres) menyala.\n2. Cek skema tabel di Database."
        
    elif task_id == 'trigger_ml_pipeline':
        diagnosis = "WARNING: Machine Learning Training Gagal."
        possible_fix = "1. Cek apakah data processed tersedia.\n2. Cek penggunaan Memori/RAM Docker."
    
    elif task_id == 'perform_auto_backup':
        diagnosis = "MINOR: Gagal melakukan Backup Otomatis."
        possible_fix = "Cek izin tulis (permission) pada folder backups."

    # -------------------------------------------------------------

    # 4. Buat Pesan Discord
    payload = {
        "username": "Toyota Data Warehouse Guard",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        "embeds": [
            {
                "title": "🚨 DISASTER DETECTED! (Pipeline Failure)",
                "description": f"**Diagnosis:** {diagnosis}",
                "color": 15548997, # Merah
                "fields": [
                    {"name": "Recommended Action", "value": f"```{possible_fix}```", "inline": False},
                    {"name": "Failed Task", "value": f"`{task_id}`", "inline": True},
                    {"name": "DAG ID", "value": f"`{dag_id}`", "inline": True},
                    {"name": "Time", "value": f"{execution_date}", "inline": False},
                    {"name": "System Raw Error", "value": f"_{str(exception)[:100]}..._", "inline": False}
                ],
                "footer": {"text": "Toyota BI Disaster Recovery System"},
                "timestamp": datetime.utcnow().isoformat()
            }
        ],
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "View Logs & Fix",
                        "style": 5, 
                        "url": log_url
                    }
                ]
            }
        ]
    }

    # 5. Kirim Request
    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 204:
            print("[SUCCESS] Smart Alert sent to Discord!")
        else:
            print(f"[ERROR] Discord refused: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")