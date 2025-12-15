import shutil
import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from config.paths import PROCESSED_DATA_DIR, BASE_DIR
from config.database import get_dw_connection_string

class BackupManager:
    """Manages Data Backup & Recovery Operations"""
    
    def __init__(self):
        # Folder khusus backup
        self.backup_dir = BASE_DIR / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        
    def perform_full_backup(self):
        """
        Backup Strategy 1: File-Level Backup
        Mencadangkan file CSV hasil proses (Processed Data).
        """
        print("[BACKUP] Starting File-Level Backup...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Backup File CSV Utama
        source_file = PROCESSED_DATA_DIR / 'Car_Sales_Toyota_USA.csv'
        
        if source_file.exists():
            backup_filename = f"BACKUP_Car_Sales_{timestamp}.csv"
            dest_file = self.backup_dir / backup_filename
            
            try:
                shutil.copy2(source_file, dest_file)
                print(f"   File Backup created: {dest_file}")
            except Exception as e:
                print(f"   File Backup failed: {e}")
        else:
            print("   Source file not found, skipping file backup.")

        # 2. Backup Database Snapshot (Strategy 2)
        self._backup_database_snapshot(timestamp)
        
        return True

    def _backup_database_snapshot(self, timestamp):
        """
        Backup Strategy 2: Database-Level Backup
        Mengekspor tabel fakta utama langsung dari Database.
        """
        print("[BACKUP] Starting Database Snapshot...")
        try:
            from sqlalchemy import create_engine
            engine = create_engine(get_dw_connection_string())
            
            # Ekspor Tabel Fakta Penjualan
            query = 'SELECT * FROM "FactSales"'
            df = pd.read_sql(query, engine)
            
            if not df.empty:
                filename = f"SNAPSHOT_FactSales_{timestamp}.csv"
                path = self.backup_dir / filename
                df.to_csv(path, index=False)
                print(f"   Database Snapshot created: {path} ({len(df)} records)")
            else:
                print("   FactSales table is empty.")
                
        except Exception as e:
            print(f"   Database Snapshot failed: {e}")

if __name__ == "__main__":
    bm = BackupManager()
    bm.perform_full_backup()