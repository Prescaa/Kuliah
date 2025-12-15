import pandas as pd
import numpy as np
import requests
import time
import json
import os
import concurrent.futures
import warnings  # Tambahan untuk handle warning
from datetime import datetime
from datalake.minio_setup import DataLakeManager
from config.paths import ENTERPRISE_RAW_DIR, PROCESSED_DATA_DIR

# Suppress specific pandas warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

class ETLTransformer:
    """Main ETL transformation logic with Self-Healing Capability"""
    
    def __init__(self):
        self.datalake = DataLakeManager()
        self.api_base_url = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
        self.cache_file = PROCESSED_DATA_DIR / 'nhtsa_cache.json'
        
    def run_transform(self):
        print("\n" + "="*60)
        print("[INFO] STARTING ETL TRANSFORMATION PIPELINE")
        print("="*60)
        
        # --- PHASE 1: INGESTION ---
        print("\n[PHASE 1] Loading Data Sources...")
        df_sales = self._load_sales_data()
        df_fuel = self._load_fuel_data()
        df_geo = self._load_geo_data()
        df_cpi = self._load_cpi_data()
        
        # --- PHASE 2: TRANSFORMATION ---
        print("\n[PHASE 2] Cleaning & Transforming Sales Data...")
        df_toyota = self._transform_sales(df_sales)
        df_toyota = self._add_origin_country(df_toyota)
        
        # --- PHASE 3: ENRICHMENT (API) ---
        print("\n[PHASE 3] API Enrichment (NHTSA Safety Data)...")
        df_toyota = self._add_complaint_data_parallel(df_toyota)
        
        # --- PHASE 4: MERGING & FINALIZING ---
        print("\n[PHASE 4] Merging Datasets & Finalizing...")
        df_final = self._merge_datasets(df_toyota, df_fuel, df_geo, df_cpi)
        df_final = self._add_business_metrics(df_final)
        
        # --- PHASE 5: SAVING ---
        print("\n[PHASE 5] Saving Results...")
        self._save_results(df_final)
        
        print("\n" + "="*60)
        print("[SUCCESS]  ETL Transformation Complete!")
        print("="*60 + "\n")
        return df_final

    def _smart_load(self, target_filename, minio_bucket, minio_prefix, search_keyword):
        local_path = ENTERPRISE_RAW_DIR / target_filename
        
        # Skenario 1: File ada di lokal
        if local_path.exists():
            return pd.read_csv(local_path, on_bad_lines='skip', low_memory=False)
        
        # Skenario 2: File hilang -> Recovery
        print(f"     [WARN] File {target_filename} missing locally. Initiating Recovery...")
        
        try:
            objects = self.datalake.list_files(minio_bucket, prefix=minio_prefix)
            candidates = [obj for obj in objects if search_keyword in obj]
            
            if not candidates:
                raise FileNotFoundError(f"Critical: Backup for {target_filename} not found in Data Lake!")
            
            latest_backup = sorted(candidates)[-1]
            print(f"   🔄 [RECOVERY] Found backup: {latest_backup}")
            print(f"   ⬇️  [RECOVERY] Downloading to local staging...")
            
            self.datalake.client.fget_object(minio_bucket, latest_backup, str(local_path))
            
            print(f"    [SUCCESS] File recovered. Resuming...")
            return pd.read_csv(local_path, on_bad_lines='skip', low_memory=False)
            
        except Exception as e:
            print(f"    [ERROR] Auto-Recovery failed: {e}")
            raise

    def _load_sales_data(self):
        df = self._smart_load('TRX_AutoAuctions.csv', 'raw-data', 'auctions/', 'car_prices')
        df['make'] = df['make'].astype(str).str.title().str.strip()
        df_toyota = df[df['make'] == 'Toyota'].copy()
        print(f"   -> Loaded {len(df_toyota):,} Toyota sales records")
        return df_toyota
    
    def _load_fuel_data(self):
        df = self._smart_load('REF_FuelEconomy.csv', 'raw-data', 'fuel_economy/', 'fuel')
        print(f"   -> Loaded {len(df):,} fuel economy records")
        return df
    
    def _load_geo_data(self):
        df = self._smart_load('REF_GeoLocation.csv', 'raw-data', 'geography/', 'uscities')
        print(f"   -> Loaded {len(df):,} geographic records")
        return df
    
    def _load_cpi_data(self):
        df = self._smart_load('EXT_US_CPI_Inflation.csv', 'raw-data', 'inflation/', 'cpi')
        print(f"   -> Loaded {len(df):,} inflation records")
        return df
    
    def _transform_sales(self, df):
        # Menggunakan context manager untuk menangkap warning spesifik di block ini saja jika global filter tidak cukup
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df['saledate'] = pd.to_datetime(df['saledate'], utc=True, errors='coerce')
            
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(2000).astype(int)
        df['sellingprice'] = pd.to_numeric(df['sellingprice'], errors='coerce')
        df['mmr'] = pd.to_numeric(df['mmr'], errors='coerce')
        df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(df['odometer'].median())
        df['condition'] = pd.to_numeric(df['condition'], errors='coerce').fillna(3.0)
        df['state'] = df['state'].astype(str).str.upper().str.strip()
        df['model'] = df['model'].astype(str).str.strip().str.upper()
        df = df.dropna(subset=['saledate', 'sellingprice', 'mmr'])
        print("   -> Sales data cleaned & standardized")
        return df
    
    def _add_origin_country(self, df):
        def get_origin(vin):
            if pd.isna(vin): return 'Unknown'
            vin_str = str(vin)
            if len(vin_str) < 1: return 'Unknown'
            code = vin_str[0].upper()
            if code == 'J': return 'Japan'
            if code in ['1', '4', '5']: return 'USA'
            if code == '2': return 'Canada'
            if code == '3': return 'Mexico'
            if code == 'S': return 'UK'
            if code == 'K': return 'Korea'
            return 'Other'
        df['OriginCountry'] = df['vin'].apply(get_origin)
        print("   -> Origin country derived from VIN")
        return df

    def _call_api(self, make, model, year):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {"make": make, "model": model, "modelYear": year}
        try:
            response = requests.get(self.api_base_url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('count', 0)
        except:
            pass
        return 0

    def _fetch_single_vehicle_smart(self, vehicle_tuple):
        make, model, year = vehicle_tuple
        count = self._call_api(make, model, year)
        if count == 0 and " " in model:
            simple_model = model.split(" ")[0] 
            count = self._call_api(make, simple_model, year)
        return (f"{make}_{model}_{year}", count)

    def _add_complaint_data_parallel(self, df):
        cache_data = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                print(f"   -> Loaded {len(cache_data)} records from local cache.")
            except:
                print("   -> Cache file corrupted, starting fresh.")
        
        unique_vehicles = df[['make', 'model', 'year']].drop_duplicates()
        to_fetch = []
        
        for _, row in unique_vehicles.iterrows():
            key = f"{row['make']}_{row['model']}_{row['year']}"
            if key not in cache_data or cache_data[key] == 0:
                to_fetch.append((row['make'], row['model'], row['year']))
        
        if to_fetch:
            print(f"   -> Fetching {len(to_fetch)} new configurations from API...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_car = {executor.submit(self._fetch_single_vehicle_smart, car): car for car in to_fetch}
                
                completed = 0
                for future in concurrent.futures.as_completed(future_to_car):
                    key_str, count = future.result()
                    cache_data[key_str] = count
                    
                    completed += 1
                    if completed % 10 == 0 or completed == len(to_fetch):
                        print(f"      [{completed}/{len(to_fetch)}] Processed: {key_str} -> {count} complaints")
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
            print("   -> Cache updated successfully.")
        else:
            print("   -> Using fully cached data (No API calls needed).")

        def get_count(row):
            key = f"{row['make']}_{row['model']}_{row['year']}"
            return cache_data.get(key, 0)

        df['ComplaintCount'] = df.apply(get_count, axis=1)
        return df

    def _merge_datasets(self, df_toyota, df_fuel, df_geo, df_cpi):
        # Prepare Fuel Data
        df_fuel['model_key'] = df_fuel['model'].astype(str).str.upper().str.strip()
        df_fuel['year_key'] = pd.to_numeric(df_fuel['year'], errors='coerce').fillna(0).astype(int)
        
        df_fuel_agg = df_fuel.groupby(['year_key', 'model_key'])[[
            'city_mpg_ft1', 'highway_mpg_ft1', 'fuel_type_1'
        ]].agg({
            'city_mpg_ft1': 'mean',
            'highway_mpg_ft1': 'mean',
            'fuel_type_1': 'first'
        }).reset_index()
        
        df_merged = pd.merge(
            df_toyota, df_fuel_agg, how='left',
            left_on=['year', 'model'], right_on=['year_key', 'model_key']
        )
        
        # Fill defaults
        df_merged['city_mpg_ft1'] = df_merged['city_mpg_ft1'].fillna(25.0)
        df_merged['highway_mpg_ft1'] = df_merged['highway_mpg_ft1'].fillna(32.0)
        df_merged['fuel_type_1'] = df_merged['fuel_type_1'].fillna('Regular Gasoline')
        
        # Merge CPI
        df_cpi['Year'] = df_cpi['Year'].astype(int)
        df_merged = pd.merge(df_merged, df_cpi, how='left', left_on='year', right_on='Year')
        df_merged['Inflation_Rate'] = df_merged['Inflation_Rate'].fillna(1.5)
        
        # Merge Geo
        df_geo_sorted = df_geo.sort_values('population', ascending=False)
        state_map = df_geo_sorted.groupby('state_id')['city'].first().to_dict()
        df_merged['City'] = df_merged['state'].map(state_map).fillna("Unknown")
        
        print("   -> All datasets merged successfully")
        return df_merged
    
    def _add_business_metrics(self, df):
        num_rows = len(df)
        df['CustomerID'] = range(10001, 10001 + num_rows)
        df['CustomerName'] = "Customer_" + df['CustomerID'].astype(str)
        df['Gender'] = np.random.choice(['Male', 'Female'], num_rows, p=[0.6, 0.4])
        df['Age'] = np.random.randint(21, 70, size=num_rows)
        df['CommissionEarned'] = round(df['sellingprice'] * 0.05, 2)
        print("   -> Business metrics & synthetic customers added")
        return df
    
    def _save_results(self, df):
        df_final = pd.DataFrame()
        df_final['Date'] = df['saledate']
        df_final['SalePrice'] = df['sellingprice']
        df_final['MarketPrice_MMR'] = df['mmr']
        df_final['CommissionEarned'] = df['CommissionEarned']
        df_final['InflationRate'] = df['Inflation_Rate']
        
        df_final['CarMake'] = df['make']
        df_final['CarModel'] = df['model']
        df_final['CarYear'] = df['year']
        df_final['Odometer'] = df['odometer']
        df_final['Condition'] = df['condition']
        df_final['CityMPG'] = df['city_mpg_ft1']
        df_final['HighwayMPG'] = df['highway_mpg_ft1']
        df_final['FuelType'] = df['fuel_type_1']
        df_final['ComplaintCount'] = df['ComplaintCount']
        df_final['OriginCountry'] = df['OriginCountry']
        
        df_final['CustomerID'] = df['CustomerID']
        df_final['CustomerName'] = df['CustomerName']
        df_final['Gender'] = df['Gender']
        df_final['Age'] = df['Age']
        df_final['SellerName'] = "AutoAuction_Official"
        df_final['City'] = df['City']
        df_final['State'] = df['state']
        
        output_file = PROCESSED_DATA_DIR / 'Car_Sales_Toyota_USA.csv'
        df_final.to_csv(output_file, index=False, sep=';')
        
        # Save to staging
        self.datalake.save_to_staging(df_final, "transform", "toyota_sales_transformed.csv")
        
        # Save to processed-data
        self.datalake.save_to_processed(df_final, "toyota_sales_final.csv")
        
        print(f"   -> Local Output: {output_file}")
        print(f"   -> Record Count: {len(df_final):,} rows")

def main():
    transformer = ETLTransformer()
    df_final = transformer.run_transform()

if __name__ == "__main__":
    main()