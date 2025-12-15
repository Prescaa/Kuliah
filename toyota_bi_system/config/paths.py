import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data paths
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
ENTERPRISE_RAW_DIR = BASE_DIR / 'data' / 'enterprise_raw'
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'

# Data Lake paths
DATALAKE_DIR = BASE_DIR / 'datalake'
DATALAKE_RAW = DATALAKE_DIR / 'raw'
DATALAKE_STAGING = DATALAKE_DIR / 'staging'

# ML paths
ML_DIR = BASE_DIR / 'ml'
MODELS_DIR = ML_DIR / 'models'

# Dashboard paths
DASHBOARD_DIR = BASE_DIR / 'dashboard'

# Create directories
for directory in [RAW_DATA_DIR, ENTERPRISE_RAW_DIR, PROCESSED_DATA_DIR, 
                  DATALAKE_RAW, DATALAKE_STAGING, MODELS_DIR, DASHBOARD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Subdirectories for data lake
for source in ['nhtsa', 'auctions', 'fuel_economy', 'inflation', 'geography']:
    (DATALAKE_RAW / source).mkdir(parents=True, exist_ok=True)
    (DATALAKE_STAGING / source).mkdir(parents=True, exist_ok=True)