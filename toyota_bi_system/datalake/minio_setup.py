import os
import json
import pandas as pd
from minio import Minio
from minio.error import S3Error
from datetime import datetime
from config.paths import DATALAKE_RAW, DATALAKE_STAGING

class DataLakeManager:
    """Manages Data Lake operations with MinIO"""
    
    def __init__(self, use_minio=True):
        self.use_minio = use_minio
        
        # Cek apakah sedang berjalan di dalam Docker (Airflow) atau Lokal
        # Kita gunakan AIRFLOW_HOME sebagai indikator lingkungan Docker Airflow
        is_in_docker = os.getenv('AIRFLOW_HOME') is not None
        
        # Set endpoint sesuai environment
        # Docker: panggil nama service 'minio'
        # Lokal: panggil 'localhost'
        self.minio_endpoint = "minio:9000" if is_in_docker else "localhost:9000"
        
        if use_minio:
            try:
                self.client = Minio(
                    self.minio_endpoint,
                    access_key="minioadmin",
                    secret_key="minioadmin",
                    secure=False
                )
                self.setup_buckets()
                print(f"[INFO] Connected to MinIO Data Lake at {self.minio_endpoint}")
            except Exception as e:
                print(f"[WARN] MinIO not available at {self.minio_endpoint}, using local filesystem: {e}")
                self.use_minio = False
        
    def setup_buckets(self):
        """Create buckets if they don't exist"""
        buckets = ["raw-data", "staging-data", "processed-data"]
        for bucket in buckets:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
                    print(f"[INFO] Created bucket: {bucket}")
            except S3Error as e:
                print(f"[ERROR] Error creating bucket {bucket}: {e}")
    
    def upload_raw(self, file_path, data_source, file_format="csv"):
        """Upload raw data to data lake"""
        try:
            file_name = os.path.basename(file_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            object_name = f"{data_source}/{timestamp}_{file_name}"
            
            if self.use_minio:
                self.client.fput_object(
                    "raw-data", object_name, file_path
                )
                print(f"[UPLOAD] Uploaded to MinIO: raw-data/{object_name}")
            else:
                # Save locally as fallback
                local_path = DATALAKE_RAW / data_source / f"{timestamp}_{file_name}"
                
                # Ensure directory exists
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                if file_format == "csv":
                    df = pd.read_csv(file_path)
                    df.to_csv(local_path, index=False)
                elif file_format == "json":
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    with open(local_path, 'w') as f:
                        json.dump(data, f, indent=2)
                print(f"[UPLOAD] Saved locally: {local_path}")
            
            return object_name
            
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None
    
    def save_to_staging(self, df, data_source, file_name):
        """Save intermediate data to staging area"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            staging_file = f"{timestamp}_{file_name}"
            
            if self.use_minio:
                # Convert DataFrame to CSV string
                csv_data = df.to_csv(index=False)
                self.client.put_object(
                    "staging-data",
                    f"{data_source}/{staging_file}",
                    data=pd.io.common.BytesIO(csv_data.encode()),
                    length=len(csv_data),
                    content_type='application/csv'
                )
                print(f"[STAGING] Saved to staging: {data_source}/{staging_file}")
            else:
                # Save locally
                local_path = DATALAKE_STAGING / data_source / staging_file
                
                # Ensure directory exists
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                df.to_csv(local_path, index=False)
                print(f"[STAGING] Saved locally to staging: {local_path}")
            
            return staging_file
            
        except Exception as e:
            print(f"[ERROR] Staging save failed: {e}")
            return None

    def save_to_processed(self, df, file_name):
        """Save final clean data to processed-data bucket"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            processed_file = f"{timestamp}_{file_name}"
            
            if self.use_minio:
                # Use semicolon (;) separator to match local file
                csv_data = df.to_csv(index=False, sep=';')
                
                self.client.put_object(
                    "processed-data",
                    processed_file,
                    data=pd.io.common.BytesIO(csv_data.encode()),
                    length=len(csv_data),
                    content_type='application/csv'
                )
                print(f"[PROCESSED] Saved to Data Lake: processed-data/{processed_file}")
            else:
                # Local fallback not critical as ETL already saves to local disk
                pass
            
            return processed_file
            
        except Exception as e:
            print(f"[ERROR] Processed save failed: {e}")
            return None
    
    def list_files(self, bucket, prefix=""):
        """List files in data lake"""
        if self.use_minio:
            try:
                objects = self.client.list_objects(bucket, prefix=prefix, recursive=True)
                return [obj.object_name for obj in objects]
            except S3Error as e:
                print(f"[ERROR] Error listing files: {e}")
                return []
        else:
            # List local files logic
            if bucket == "raw-data":
                base_dir = DATALAKE_RAW
            elif bucket == "staging-data":
                base_dir = DATALAKE_STAGING
            else:
                base_dir = DATALAKE_RAW
            
            search_dir = base_dir / prefix
            if search_dir.exists():
                return [str(f.relative_to(base_dir)) for f in search_dir.rglob("*") if f.is_file()]
            return []