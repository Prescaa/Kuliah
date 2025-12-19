import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime
from config.database import get_dw_connection_string
from config.paths import PROCESSED_DATA_DIR

class DimensionLoader:
    """Load dimension tables into Data Warehouse"""
    
    def __init__(self):
        self.engine = create_engine(get_dw_connection_string())
        self.csv_path = PROCESSED_DATA_DIR / 'Car_Sales_Toyota_USA.csv'
        
    def load_all_dimensions(self):
        """Load all dimension tables"""
        print("📦 Loading dimension tables...")
        
        if not self.csv_path.exists():
            print(f"❌ Processed data not found: {self.csv_path}")
            return False
        
        # Read processed data
        try:
            df = pd.read_csv(self.csv_path, sep=';')
            df['Date'] = pd.to_datetime(df['Date'])
            
            # 1. DimCar
            self._load_dim_car(df)
            
            # 2. DimLocation
            self._load_dim_location(df)
            
            # 3. DimCustomer
            self._load_dim_customer(df)
            
            # 4. DimSeller
            self._load_dim_seller(df)
            
            # 5. DimDate
            self._load_dim_date(df)
            
            print("✅ All dimension tables loaded successfully!")
            return True

        except Exception as e:
            print(f"❌ Error loading dimensions: {e}")
            return False
    
    def _load_dim_car(self, df):
        """Load DimCar table"""
        print("   🚗 Creating DimCar...")
        
        dim_car = df[[
            'CarMake', 'CarModel', 'CarYear', 'Odometer', 'Condition',
            'CityMPG', 'HighwayMPG', 'FuelType', 'ComplaintCount', 'OriginCountry'
        ]].drop_duplicates().reset_index(drop=True)
        
        dim_car['VehicleKey'] = range(1, len(dim_car) + 1)
        dim_car['CreatedDate'] = datetime.now()
        dim_car['UpdatedDate'] = datetime.now()
        
        # Load to database (SQLAlchemy otomatis handle casing saat create table)
        dim_car.to_sql('DimCar', self.engine, if_exists='replace', index=False)
        print(f"      ✅ DimCar: {len(dim_car)} records")
        
        return dim_car
    
    def _load_dim_location(self, df):
        """Load DimLocation table"""
        print("   📍 Creating DimLocation...")
        
        dim_loc = df[['City', 'State']].drop_duplicates().reset_index(drop=True)
        dim_loc['LocationKey'] = range(1, len(dim_loc) + 1)
        dim_loc['CreatedDate'] = datetime.now()
        dim_loc['UpdatedDate'] = datetime.now()
        
        dim_loc.to_sql('DimLocation', self.engine, if_exists='replace', index=False)
        print(f"      ✅ DimLocation: {len(dim_loc)} records")
        
        return dim_loc
    
    def _load_dim_customer(self, df):
        """Load DimCustomer table"""
        print("   👤 Creating DimCustomer...")
        
        dim_cust = df[['CustomerID', 'CustomerName', 'Gender', 'Age']].drop_duplicates().reset_index(drop=True)
        dim_cust['CustomerKey'] = range(1, len(dim_cust) + 1)
        dim_cust['CreatedDate'] = datetime.now()
        dim_cust['UpdatedDate'] = datetime.now()
        
        dim_cust.to_sql('DimCustomer', self.engine, if_exists='replace', index=False)
        print(f"      ✅ DimCustomer: {len(dim_cust)} records")
        
        return dim_cust
    
    def _load_dim_seller(self, df):
        """Load DimSeller table"""
        print("   🏪 Creating DimSeller...")
        
        dim_seller = df[['SellerName']].drop_duplicates().reset_index(drop=True)
        dim_seller['SellerKey'] = range(1, len(dim_seller) + 1)
        dim_seller['CreatedDate'] = datetime.now()
        dim_seller['UpdatedDate'] = datetime.now()
        
        dim_seller.to_sql('DimSeller', self.engine, if_exists='replace', index=False)
        print(f"      ✅ DimSeller: {len(dim_seller)} records")
        
        return dim_seller
    
    def _load_dim_date(self, df):
        """Load DimDate table"""
        print("   📅 Creating DimDate...")
        
        dates = df[['Date']].drop_duplicates().sort_values('Date').reset_index(drop=True)
        
        dim_date = pd.DataFrame()
        dim_date['DateKey'] = dates['Date'].dt.strftime('%Y%m%d').astype(int)
        dim_date['FullDate'] = dates['Date']
        dim_date['Year'] = dates['Date'].dt.year
        dim_date['Month'] = dates['Date'].dt.month
        dim_date['Day'] = dates['Date'].dt.day
        dim_date['Quarter'] = dates['Date'].dt.quarter
        dim_date['DayOfWeek'] = dates['Date'].dt.day_name()
        dim_date['IsWeekend'] = dates['Date'].dt.dayofweek >= 5
        dim_date['CreatedDate'] = datetime.now()
        
        dim_date.to_sql('DimDate', self.engine, if_exists='replace', index=False)
        print(f"      ✅ DimDate: {len(dim_date)} records")
        
        return dim_date
    
    def get_dimension_keys(self):
        """Retrieve dimension keys for fact table loading"""
        try:
            with self.engine.connect() as conn:
                # PERBAIKAN DI SINI:
                # Kita gunakan tanda kutip dua ("NamaTabel") agar PostgreSQL membaca 
                # huruf Besar-Kecil (Case Sensitive) dengan benar.
                
                car_map = pd.read_sql('SELECT "VehicleKey", "CarMake", "CarModel", "CarYear", "Odometer", "Condition" FROM "DimCar"', conn)
                loc_map = pd.read_sql('SELECT "LocationKey", "City", "State" FROM "DimLocation"', conn)
                cust_map = pd.read_sql('SELECT "CustomerKey", "CustomerID", "CustomerName" FROM "DimCustomer"', conn)
                seller_map = pd.read_sql('SELECT "SellerKey", "SellerName" FROM "DimSeller"', conn)
                
                return {
                    'car': car_map,
                    'location': loc_map,
                    'customer': cust_map,
                    'seller': seller_map
                }
                
        except Exception as e:
            print(f"❌ Error getting dimension keys: {e}")
            return None