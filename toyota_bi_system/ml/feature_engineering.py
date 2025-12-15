import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from config.database import get_dw_connection_string
from config.paths import PROCESSED_DATA_DIR, MODELS_DIR
import pickle
import os
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

class FeatureEngineer:
    """Feature engineering for ML model with Smart Cleaning"""
    
    def __init__(self):
        self.engine = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def load_data_from_dw(self):
        """Load data from Data Warehouse view"""
        print("   -> Connecting to Data Warehouse...")
        
        try:
            self.engine = get_dw_connection_string()
            
            # Load ALL data first
            query = """
            SELECT 
                "CarMake", "CarModel", "CarYear", "Odometer", "Condition",
                "CityMPG", "HighwayMPG", "InflationRate", "ComplaintCount", 
                "OriginCountry", "FuelType", "State",
                "SalePrice", "MarketPrice_MMR"
            FROM fact_sales
            """
            
            df = pd.read_sql(query, self.engine)
            print(f"   -> Loaded {len(df):,} records from DW (Raw)")
            return df
            
        except Exception as e:
            print(f"   [ERROR] Error loading from DW: {e}")
            return self._load_from_csv()
    
    def _load_from_csv(self):
        """Fallback: Load from processed CSV"""
        csv_path = PROCESSED_DATA_DIR / 'Car_Sales_Toyota_USA.csv'
        if csv_path.exists():
            print(f"   [WARN] Falling back to CSV: {csv_path}")
            df = pd.read_csv(csv_path, sep=';')
            return df
        else:
            raise FileNotFoundError("No data source available")

    def _representative_sampling(self, df, target_rows=1000):
        """Melakukan sampling 1000 baris yang mewakili setiap Model dan Tahun."""
        print(f"   -> Performing Representative Sampling (Target: {target_rows})...")
        
        grouped = df.groupby(['CarModel', 'CarYear'])
        # Ambil minimal 1 sampel dari tiap grup unik agar variasi terjaga
        representative_df = grouped.apply(lambda x: x.sample(1) if len(x) > 0 else x).reset_index(drop=True)
        
        current_count = len(representative_df)
        
        if current_count < target_rows:
            needed = target_rows - current_count
            remaining_data = df.drop(representative_df.index, errors='ignore')
            
            if len(remaining_data) >= needed:
                extra_samples = remaining_data.sample(n=needed, random_state=42)
            else:
                extra_samples = remaining_data
                
            final_df = pd.concat([representative_df, extra_samples]).sample(frac=1, random_state=42).reset_index(drop=True)
        else:
            final_df = representative_df.sample(n=target_rows, random_state=42).reset_index(drop=True)
            
        print(f"   -> Data reduced to {len(final_df)} rows (Stratified Sample)")
        return final_df
    
    def engineer_features(self, df):
        """Create features for ML model with SMART CLEANING"""
        
        # 1. Sampling
        df = self._representative_sampling(df, target_rows=1000)
        
        # 2. SMART CLEANING: MPG
        df['CityMPG'] = pd.to_numeric(df['CityMPG'], errors='coerce')
        df['HighwayMPG'] = pd.to_numeric(df['HighwayMPG'], errors='coerce')
        
        df.loc[df['CityMPG'] < 5, 'CityMPG'] = np.nan
        df.loc[df['HighwayMPG'] < 5, 'HighwayMPG'] = np.nan
        
        print("   -> Imputing missing MPG using Car Model averages...")
        df['CityMPG'] = df['CityMPG'].fillna(df.groupby('CarModel')['CityMPG'].transform('median'))
        df['HighwayMPG'] = df['HighwayMPG'].fillna(df.groupby('CarModel')['HighwayMPG'].transform('median'))
        
        df['CityMPG'] = df['CityMPG'].fillna(df['CityMPG'].median()).round(1)
        df['HighwayMPG'] = df['HighwayMPG'].fillna(df['HighwayMPG'].median()).round(1)
        
        # 3. FIX: Condition Cleaning
        df['Condition'] = pd.to_numeric(df['Condition'], errors='coerce').fillna(3.0)
        
        # 4. Categorical encoding
        categorical_cols = ['CarModel', 'State', 'OriginCountry', 'FuelType']
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[f'{col}_Code'] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # 5. Feature Creation
        current_year = 2024
        df['VehicleAge'] = current_year - df['CarYear']
        
        # Price Ratio Fix
        df['Price_vs_MMR_Ratio'] = np.where(
            df['MarketPrice_MMR'] > 0,
            df['SalePrice'] / df['MarketPrice_MMR'],
            1.0
        )
        
        df['AvgMPG'] = (df['CityMPG'] + df['HighwayMPG']) / 2
        
        # 6. Condition Grouping Fix
        conditions = [
            (df['Condition'] < 2.0),
            (df['Condition'] >= 2.0) & (df['Condition'] < 3.6),
            (df['Condition'] >= 3.6)
        ]
        choices = ['Poor', 'Average', 'Excellent']
        df['Condition_Group'] = np.select(conditions, choices, default='Average')
            
        le_condition = LabelEncoder()
        df['Condition_Code'] = le_condition.fit_transform(df['Condition_Group'].astype(str))
        self.label_encoders['Condition_Group'] = le_condition
        
        # Mileage per year
        df['MilesPerYear'] = np.where(
            df['VehicleAge'] > 0,
            df['Odometer'] / df['VehicleAge'],
            df['Odometer']
        )
        
        # Final Feature Selection
        feature_cols = [
            'CarYear', 'Odometer', 'Condition', 'VehicleAge',
            'CityMPG', 'HighwayMPG', 'AvgMPG', 'MilesPerYear',
            'InflationRate', 'ComplaintCount',
            'CarModel_Code', 'State_Code', 'OriginCountry_Code',
            'FuelType_Code', 'Condition_Code',
            'Price_vs_MMR_Ratio'
        ]
        
        available_features = [col for col in feature_cols if col in df.columns]
        X = df[available_features]
        y = df['SalePrice']
        
        print(f"   -> Created {len(available_features)} engineered features")
        return X, y, df
    
    def split_data(self, X, y, test_size=0.2):
        print(f"   -> Splitting data (Train: {1-test_size:.0%} / Test: {test_size:.0%})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        return X_train, X_test, y_train, y_test
    
    def scale_features(self, X_train, X_test):
        print("   -> Scaling numerical features (StandardScaler)...")
        numerical_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        # Fit on Train
        X_train_scaled[numerical_cols] = self.scaler.fit_transform(X_train[numerical_cols])
        # Transform Test
        X_test_scaled[numerical_cols] = self.scaler.transform(X_test[numerical_cols])
        
        return X_train_scaled, X_test_scaled, numerical_cols
    
    def save_encoders(self):
        save_dir = MODELS_DIR / 'preprocessing'
        save_dir.mkdir(exist_ok=True, parents=True)
        
        for col, encoder in self.label_encoders.items():
            with open(save_dir / f'label_encoder_{col}.pkl', 'wb') as f:
                pickle.dump(encoder, f)
        
        with open(save_dir / 'standard_scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"   -> Preprocessing objects saved to {save_dir}")
        return save_dir

def main():
    print("\n" + "="*60)
    print("[INFO] STARTING FEATURE ENGINEERING PIPELINE")
    print("="*60)
    
    engineer = FeatureEngineer()
    
    # Phase 1: Load
    print("\n[PHASE 1] Data Loading")
    df = engineer.load_data_from_dw()
    
    # Phase 2: Engineering
    print("\n[PHASE 2] Feature Engineering & Cleaning")
    X, y, df_full = engineer.engineer_features(df)
    
    # Phase 3: Split & Scale
    print("\n[PHASE 3] Preprocessing")
    X_train, X_test, y_train, y_test = engineer.split_data(X, y)
    X_train_scaled, X_test_scaled, num_cols = engineer.scale_features(X_train, X_test)
    
    # --- BARU: Prepare X_full_scaled untuk output BI (1000 baris) ---
    print("   -> Preparing Full Dataset for BI Output...")
    X_full_scaled = X.copy()
    X_full_scaled[num_cols] = engineer.scaler.transform(X[num_cols])
    # ---------------------------------------------------------------
    
    # Phase 4: Save
    print("\n[PHASE 4] Caching Artifacts")
    engineer.save_encoders()
    
    cache_dir = PROCESSED_DATA_DIR / 'ml_cache'
    cache_dir.mkdir(exist_ok=True, parents=True)
    
    with open(cache_dir / 'X_train.pkl', 'wb') as f: pickle.dump(X_train_scaled, f)
    with open(cache_dir / 'X_test.pkl', 'wb') as f: pickle.dump(X_test_scaled, f)
    with open(cache_dir / 'y_train.pkl', 'wb') as f: pickle.dump(y_train, f)
    with open(cache_dir / 'y_test.pkl', 'wb') as f: pickle.dump(y_test, f)
    with open(cache_dir / 'df_full.pkl', 'wb') as f: pickle.dump(df_full, f)
    with open(cache_dir / 'X_full_scaled.pkl', 'wb') as f: pickle.dump(X_full_scaled, f)
    
    print(f"   -> Data cached to: {cache_dir}")
    
    print("\n" + "="*60)
    print("[SUCCESS] FEATURE ENGINEERING COMPLETE")
    print("="*60 + "\n")
    return "Done"

if __name__ == "__main__":
    main()