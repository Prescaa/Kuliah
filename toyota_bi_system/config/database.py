import os

# Cek environment: Jika ada AIRFLOW_HOME, berarti sedang jalan di dalam Docker Airflow
IS_IN_DOCKER = os.getenv('AIRFLOW_HOME') is not None

# Database Configuration
DATABASE_CONFIG = {
    'warehouse': {
        # Jika di Docker gunakan nama service 'postgres_dw', jika lokal 'localhost'
        'host': 'postgres_dw' if IS_IN_DOCKER else 'localhost',
        # Jika di Docker gunakan port internal 5432, jika lokal gunakan port mapping 5433
        'port': '5432' if IS_IN_DOCKER else '5433',
        'database': 'toyota_warehouse',
        'user': 'admin',
        'password': 'adminpassword'
    },
    'airflow': {
        'host': 'postgres_airflow' if IS_IN_DOCKER else 'localhost',
        'port': '5432',
        'database': 'airflow',
        'user': 'airflow',
        'password': 'airflow'
    }
}

def get_dw_connection_string():
    cfg = DATABASE_CONFIG['warehouse']
    return f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"

def get_airflow_connection_string():
    cfg = DATABASE_CONFIG['airflow']
    return f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"