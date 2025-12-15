import pandas as pd
import numpy as np
import os
from datetime import datetime
from datalake.minio_setup import DataLakeManager
from config.paths import RAW_DATA_DIR, ENTERPRISE_RAW_DIR

class CSVIngestor:
    """Batch CSV ingestion with data quality checks"""
    
    def __init__(self):
        self.datalake = DataLakeManager()
        
    def ingest_file(self, file_name, data_source):
        """Ingest a CSV file with validation"""
        print(f"📥 Ingesting {file_name} from {data_source}...")
        
        source_path = RAW_DATA_DIR / file_name
        if not source_path.exists():
            print(f"❌ File not found: {source_path}")
            return None
        
        try:
            # Read CSV with error handling
            df = pd.read_csv(source_path, on_bad_lines='skip', low_memory=False)
            
            # Basic validation
            if df.empty:
                print(f"⚠️ File {file_name} is empty")
                return None
            
            print(f"   📊 Shape: {df.shape}, Columns: {list(df.columns)}")
            
            # Data quality report
            quality_report = self._generate_quality_report(df, file_name)
            
            # Upload to data lake
            self.datalake.upload_raw(source_path, data_source, "csv")
            
            # Save processed version to enterprise_raw
            enterprise_path = ENTERPRISE_RAW_DIR / file_name
            df.to_csv(enterprise_path, index=False)
            
            print(f"✅ Successfully ingested {len(df)} records")
            
            return df
            
        except Exception as e:
            print(f"❌ Error ingesting {file_name}: {e}")
            return None
    
    def _generate_quality_report(self, df, file_name):
        """Generate data quality report"""
        report = {
            'file_name': file_name,
            'timestamp': datetime.now().isoformat(),
            'row_count': len(df),
            'column_count': len(df.columns),
            'missing_values': {},
            'column_types': {}
        }
        
        # Check for missing values
        for col in df.columns:
            missing = df[col].isnull().sum()
            if missing > 0:
                report['missing_values'][col] = {
                    'count': int(missing),
                    'percentage': round((missing / len(df)) * 100, 2)
                }
        
        # Record column types
        for col in df.columns:
            report['column_types'][col] = str(df[col].dtype)
        
        # Save report
        report_file = f"quality_report_{file_name.replace('.csv', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = ENTERPRISE_RAW_DIR / report_file
        
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   📋 Quality report saved: {report_file}")
        return report
    
    def ingest_all(self):
        """Ingest all CSV files from raw directory"""
        print("🚀 Starting batch CSV ingestion...")
        
        # Map files to data sources
        file_mapping = {
            'car_prices.csv': 'auctions',
            'fuel.csv': 'fuel_economy',
            'uscities.csv': 'geography',
            'cpi_raw.csv': 'inflation'
        }
        
        results = {}
        for file_name, data_source in file_mapping.items():
            df = self.ingest_file(file_name, data_source)
            if df is not None:
                results[file_name] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'data_source': data_source
                }
        
        # Summary
        print("\n📈 INGESTION SUMMARY:")
        print("-" * 40)
        for file, stats in results.items():
            print(f"{file}: {stats['rows']} rows, {stats['columns']} cols ({stats['data_source']})")
        
        return results

def main():
    """Main function"""
    ingestor = CSVIngestor()
    results = ingestor.ingest_all()
    print(f"\n✅ Total files ingested: {len(results)}")

if __name__ == "__main__":
    main()