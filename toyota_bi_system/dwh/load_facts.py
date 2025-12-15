import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime
from config.database import get_dw_connection_string
from config.paths import PROCESSED_DATA_DIR

class FactLoader:
    """Load fact tables into Data Warehouse"""
    
    def __init__(self):
        self.engine = create_engine(get_dw_connection_string())
        self.csv_path = PROCESSED_DATA_DIR / 'Car_Sales_Toyota_USA.csv'
        
    def load_all_facts(self):
        """Load all fact tables"""
        print(" Loading fact tables...")
        
        if not self.csv_path.exists():
            print(f" Processed data not found: {self.csv_path}")
            return False
        
        # Read processed data
        df = pd.read_csv(self.csv_path, sep=';')
        df['Date'] = pd.to_datetime(df['Date'])
        
        try:
            # Get dimension keys first
            from dwh.load_dimensions import DimensionLoader
            dim_loader = DimensionLoader()
            dim_keys = dim_loader.get_dimension_keys()
            
            if dim_keys is None:
                print(" Cannot load facts without dimension keys")
                return False
            
            # 1. FactSales (transactional)
            self._load_fact_sales(df, dim_keys)
            
            # 2. FactCustomerSummary (aggregated)
            self._load_fact_customer_summary()
            
            # 3. Create views
            self._create_views()
            
            print(" All fact tables loaded successfully!")
            return True
            
        except Exception as e:
            print(f" Error loading facts: {e}")
            return False
    
    def _load_fact_sales(self, df, dim_keys):
        """Load FactSales table"""
        print("    Creating FactSales...")
        
        # Start with base data
        fact_sales = df.copy()
        
        # Merge with dimension keys to get foreign keys
        # DimCar
        fact_sales = fact_sales.merge(
            dim_keys['car'],
            on=['CarMake', 'CarModel', 'CarYear', 'Odometer', 'Condition'],
            how='left'
        )
        
        # DimLocation
        fact_sales = fact_sales.merge(
            dim_keys['location'],
            on=['City', 'State'],
            how='left'
        )
        
        # DimCustomer
        fact_sales = fact_sales.merge(
            dim_keys['customer'],
            on=['CustomerID', 'CustomerName'],
            how='left'
        )
        
        # DimSeller
        fact_sales = fact_sales.merge(
            dim_keys['seller'],
            on=['SellerName'],
            how='left'
        )
        
        # DimDate (DateKey)
        fact_sales['DateKey'] = fact_sales['Date'].dt.strftime('%Y%m%d').astype(int)
        
        # Select columns for FactSales
        final_fact = fact_sales[[
            'DateKey', 'VehicleKey', 'LocationKey', 'CustomerKey', 'SellerKey',
            'SalePrice', 'MarketPrice_MMR', 'CommissionEarned', 'InflationRate'
        ]].copy()
        
        # Generate SalesID (primary key)
        final_fact = final_fact.reset_index(drop=True)
        final_fact.index.name = 'IndexTemp'
        final_fact = final_fact.reset_index()
        final_fact = final_fact.rename(columns={'IndexTemp': 'SalesID'})
        final_fact['SalesID'] = final_fact['SalesID'] + 1
        
        # Add calculated column
        final_fact['Profit_vs_Market'] = final_fact['SalePrice'] - final_fact['MarketPrice_MMR']
        final_fact['CreatedDate'] = datetime.now()
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text('DROP TABLE IF EXISTS "FactSales" CASCADE'))
                conn.commit()
                print("        Dropped old FactSales table and dependent views")
        except Exception as e:
            print(f"       Warning dropping table: {e}")

        # Load to database
        final_fact.to_sql('FactSales', self.engine, if_exists='replace', index=False)
        print(f"       FactSales: {len(final_fact)} records")
        # -------------------------
        
        return final_fact
    
    def _load_fact_customer_summary(self):
        """Load FactCustomerSummary table"""
        print("    Creating FactCustomerSummary...")
        
        try:
            with self.engine.connect() as conn:
                # Get data from FactSales and DimDate
                query = """
                SELECT 
                    f."CustomerKey",
                    d."FullDate",
                    f."SalePrice",
                    f."CommissionEarned"
                FROM "FactSales" f
                JOIN "DimDate" d ON f."DateKey" = d."DateKey"
                """
                
                df_sales = pd.read_sql(query, conn)
                
                # Aggregate by customer
                cust_summary = df_sales.groupby('CustomerKey').agg(
                    TotalSpend=('SalePrice', 'sum'),
                    TotalTransactions=('SalePrice', 'count'),
                    AvgTransactionValue=('SalePrice', 'mean'),
                    TotalCommission=('CommissionEarned', 'sum'),
                    LastPurchaseDate=('FullDate', 'max')
                ).reset_index()
                
                # Calculate customer segments
                cust_summary['CustomerSegment'] = np.where(
                    cust_summary['TotalSpend'] > cust_summary['TotalSpend'].median(),
                    'Premium', 'Standard'
                )
                
                # Generate primary key
                cust_summary.index.name = 'CustomerSummaryID'
                cust_summary = cust_summary.reset_index()
                cust_summary['CustomerSummaryID'] = cust_summary['CustomerSummaryID'] + 1
                cust_summary['CreatedDate'] = datetime.now()
                
                # Load to database
                cust_summary.to_sql('FactCustomerSummary', self.engine, if_exists='replace', index=False)
                print(f"       FactCustomerSummary: {len(cust_summary)} records")
                
                return cust_summary
                
        except Exception as e:
            print(f"       Error creating customer summary: {e}")
            return None
    
    def _create_views(self):
        """Create business views"""
        print("    Creating business views...")
        
        try:
            with self.engine.connect() as conn:
                # Drop existing view
                conn.execute(text("DROP VIEW IF EXISTS fact_sales CASCADE"))
                conn.commit()
                
                # Create comprehensive view for ML/BI
                create_view_sql = """
                CREATE OR REPLACE VIEW fact_sales AS
                SELECT 
                    f."SalesID",
                    f."SalePrice",
                    f."MarketPrice_MMR",
                    f."CommissionEarned",
                    f."InflationRate",
                    f."Profit_vs_Market",
                    d."FullDate" as "Date",
                    d."Year",
                    d."Month",
                    d."Quarter",
                    c."CarMake",
                    c."CarModel",
                    c."CarYear",
                    c."Odometer",
                    c."Condition",
                    c."CityMPG",
                    c."HighwayMPG",
                    c."FuelType",
                    c."ComplaintCount",
                    c."OriginCountry",
                    l."City",
                    l."State",
                    cust."CustomerName",
                    cust."Gender",
                    cust."Age",
                    s."SellerName"
                FROM "FactSales" f
                JOIN "DimDate" d ON f."DateKey" = d."DateKey"
                JOIN "DimCar" c ON f."VehicleKey" = c."VehicleKey"
                JOIN "DimLocation" l ON f."LocationKey" = l."LocationKey"
                JOIN "DimCustomer" cust ON f."CustomerKey" = cust."CustomerKey"
                JOIN "DimSeller" s ON f."SellerKey" = s."SellerKey";
                """
                
                conn.execute(text(create_view_sql))
                conn.commit()
                
                # Create view for dashboard
                dashboard_view_sql = """
                CREATE OR REPLACE VIEW dashboard_data AS
                SELECT 
                    "Date",
                    "CarMake",
                    "CarModel",
                    "CarYear",
                    "SalePrice",
                    "MarketPrice_MMR",
                    "CityMPG",
                    "HighwayMPG",
                    "ComplaintCount",
                    "OriginCountry",
                    "City",
                    "State",
                    "CustomerName",
                    "Gender",
                    "Age",
                    "SellerName",
                    "Profit_vs_Market"
                FROM fact_sales;
                """
                
                conn.execute(text(dashboard_view_sql))
                conn.commit()
                
                print("       Created 2 business views")
                
        except Exception as e:
            print(f"       Error creating views: {e}")

def main():
    """Main function"""
    loader = FactLoader()
    success = loader.load_all_facts()
    
    if success:
        print("\n Fact table loading complete!")
    else:
        print("\n Fact table loading failed!")

if __name__ == "__main__":
    main()