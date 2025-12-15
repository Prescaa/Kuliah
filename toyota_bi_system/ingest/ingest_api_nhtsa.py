import requests
import pandas as pd
import time
import json
from datetime import datetime
from datalake.minio_setup import DataLakeManager
from config.api_config import API_CONFIG, MOCK_DATA

class NHTSAIngestor:
    """Ingest safety complaint data from NHTSA API"""
    
    def __init__(self, use_mock=False):
        self.base_url = API_CONFIG['nhtsa']['base_url']
        self.timeout = API_CONFIG['nhtsa']['timeout']
        self.retries = API_CONFIG['nhtsa']['retries']
        self.use_mock = use_mock
        self.datalake = DataLakeManager()
        self.session = requests.Session()
        
    def get_complaints(self, make, model, year):
        """Get safety complaints for specific vehicle"""
        if self.use_mock:
            print(f"🎭 Using mock data for {make} {model} {year}")
            try:
                return MOCK_DATA['complaints'][make][model.upper()].get(year, 25)
            except KeyError:
                return 25  # Default value
        
        url = f"{self.base_url}/complaints/complaintsByVehicle"
        params = {
            "make": make,
            "model": model,
            "year": year
        }
        
        for attempt in range(self.retries):
            try:
                print(f"🌐 Requesting: {make} {model} {year} (attempt {attempt+1})")
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                
                data = response.json()
                count = data.get('count', 0)
                
                # Save raw response
                raw_file = f"temp_nhtsa_{make}_{model}_{year}_{datetime.now().strftime('%H%M%S')}.json"
                with open(raw_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.datalake.upload_raw(raw_file, "nhtsa", "json")
                os.remove(raw_file)  # Clean up temp file
                
                print(f"✅ Found {count} complaints for {make} {model} {year}")
                return count
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Attempt {attempt+1} failed: {e}")
                if attempt < self.retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"⚠️ Using fallback value for {make} {model} {year}")
                    return 25  # Fallback value
        
        return 25  # Default fallback
    
    def process_vehicle_list(self, vehicles_df):
        """Process a dataframe of vehicles"""
        print(f"📋 Processing {len(vehicles_df)} vehicles...")
        
        complaints = []
        for idx, row in vehicles_df.iterrows():
            make = row.get('make', 'Toyota')
            model = row.get('model', '')
            year = row.get('year', 2020)
            
            if model:  # Skip empty models
                count = self.get_complaints(make, model, year)
                complaints.append({
                    'make': make,
                    'model': model,
                    'year': year,
                    'complaint_count': count,
                    'timestamp': datetime.now()
                })
            
            # Be nice to the API
            if not self.use_mock and idx % 5 == 0:
                time.sleep(0.5)
        
        # Create DataFrame and save
        if complaints:
            df = pd.DataFrame(complaints)
            
            # Save to staging
            staging_file = f"complaints_{datetime.now().strftime('%Y%m%d')}.csv"
            self.datalake.save_to_staging(df, "nhtsa", staging_file)
            
            print(f"✅ Saved {len(df)} complaint records")
            return df
        
        return pd.DataFrame()

def main():
    """Main function for testing"""
    ingestor = NHTSAIngestor(use_mock=True)  # Use mock for testing
    
    # Test with sample data
    test_vehicles = pd.DataFrame([
        {'make': 'Toyota', 'model': 'CAMRY', 'year': 2020},
        {'make': 'Toyota', 'model': 'COROLLA', 'year': 2021},
        {'make': 'Toyota', 'model': 'RAV4', 'year': 2022}
    ])
    
    result = ingestor.process_vehicle_list(test_vehicles)
    print(result.head())

if __name__ == "__main__":
    main()