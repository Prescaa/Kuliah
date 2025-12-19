import os

IS_IN_DOCKER = os.getenv('AIRFLOW_HOME') is not None

# Database Configuration
DATABASE_CONFIG = {
    'warehouse': {
        'host': 'postgres_dw' if IS_IN_DOCKER else 'localhost',
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