import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
# ----------------------------------------------------

from config.paths import MODELS_DIR, PROCESSED_DATA_DIR, BASE_DIR, DASHBOARD_DIR
import os

class ModelTrainer:
    """Train and evaluate Random Forest model (Single Model)"""
    
    def __init__(self):
        self.model = None
        self.metrics = {}
        
    def train_random_forest(self, X_train, y_train, **kwargs):
        """Train Random Forest model"""
        print("   -> Training Random Forest model...")
        
        params = {
            'n_estimators': 100,
            'max_depth': 20,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        
        params.update(kwargs)
        
        self.model = RandomForestRegressor(**params)
        self.model.fit(X_train, y_train)
        
        print(f"   -> Model trained successfully with {params['n_estimators']} trees")
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("   -> Evaluating model performance...")
        
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mse': mean_squared_error(y_test, y_pred)
        }
        
        # Cross validation
        cv_scores = cross_val_score(
            self.model, X_test, y_test, 
            cv=5, scoring='r2', n_jobs=-1
        )
        
        self.metrics['cv_r2_mean'] = cv_scores.mean()
        self.metrics['cv_r2_std'] = cv_scores.std()
        
        print("\n" + "-"*40)
        print("MODEL PERFORMANCE METRICS")
        print("-" * 40)
        print(f"R2 Score (Accuracy):   {self.metrics['r2_score']*100:.2f}%")
        print(f"Cross-Val Accuracy:    {self.metrics['cv_r2_mean']*100:.2f}% (+/- {self.metrics['cv_r2_std']*100:.2f}%)")
        print(f"MAE (Mean Abs Error):  ${self.metrics['mae']:,.0f}")
        print(f"RMSE (Root Mean Sq):   ${self.metrics['rmse']:,.0f}")
        print("-" * 40 + "\n")
        
        return self.metrics, y_pred
    
    def get_feature_importance(self, feature_names):
        """Get and display feature importance"""
        print("   -> Extracting Feature Importance...")
        
        importance = pd.DataFrame({
            'Feature': feature_names,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\n   Top 10 Most Important Features:")
        for idx, row in importance.head(10).iterrows():
            print(f"      - {row['Feature']:<20}: {row['Importance']:.4f}")
        print("")
        
        return importance
    
    def save_model(self, model_name="random_forest"):
        """Save model and metadata"""
        
        model_dir = MODELS_DIR / model_name
        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
        
        model_path = model_dir / 'model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        metrics_path = model_dir / 'metrics.json'
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        metadata = {
            'model_type': 'RandomForestRegressor',
            'training_date': datetime.now().isoformat(),
            'features_used': len(self.model.feature_importances_)
        }
        
        metadata_path = model_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   -> Model artifact saved to: {model_path}")
        return model_path
    
    def create_visualizations(self, y_test, y_pred, feature_importance, save_dir=None):
        """Create visualizations"""
        if save_dir is None:
            save_dir = MODELS_DIR / 'visualizations'
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        
        print("   -> Creating performance visualizations...")
        
        # Plot 1: Actual vs Predicted
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Price ($)')
        plt.ylabel('Predicted Price ($)')
        plt.title('Actual vs Predicted Sale Prices')
        plt.grid(True, alpha=0.3)
        plt.savefig(save_dir / 'actual_vs_predicted.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Plot 2: Feature Importance
        plt.figure(figsize=(12, 8))
        top_features = feature_importance.head(15)
        plt.barh(top_features['Feature'], top_features['Importance'])
        plt.xlabel('Importance')
        plt.title('Top 15 Feature Importances')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
        plt.savefig(save_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   -> Visualizations saved to: {save_dir}")
        return save_dir
    
    def generate_prediction_dataset(self, df_full, X_full_scaled):
        """Generate BI dataset with FUTURE FORECASTS"""
        print("\n[PHASE 4] BI Data Generation & Forecasting")
        
        # 1. Valuation
        y_pred_now = self.model.predict(X_full_scaled)
        
        df_results = df_full.copy()
        df_results['Predicted_Price'] = y_pred_now
        
        # 2. Forecasting Simulation
        print("   -> Running Forecast Simulation (1 & 3 Years later)...")
        
        # Scenario 1: +1 Year
        X_future_1y = X_full_scaled.copy()
        if 'VehicleAge' in X_future_1y.columns:
            X_future_1y['VehicleAge'] += 1
        if 'Odometer' in X_future_1y.columns and 'MilesPerYear' in X_future_1y.columns:
            X_future_1y['Odometer'] += X_future_1y['MilesPerYear']
            
        y_pred_1y = self.model.predict(X_future_1y)
        df_results['Forecast_1_Year'] = y_pred_1y
        
        # Scenario 2: +3 Years
        X_future_3y = X_full_scaled.copy()
        if 'VehicleAge' in X_future_3y.columns:
            X_future_3y['VehicleAge'] += 3
        if 'Odometer' in X_future_3y.columns and 'MilesPerYear' in X_future_3y.columns:
            X_future_3y['Odometer'] += (X_future_3y['MilesPerYear'] * 3)
            
        y_pred_3y = self.model.predict(X_future_3y)
        df_results['Forecast_3_Year'] = y_pred_3y
        
        # Calc Depreciation %
        df_results['Depreciation_3Y_Pct'] = ((df_results['Predicted_Price'] - df_results['Forecast_3_Year']) / df_results['Predicted_Price']) * 100
        
        # 3. Calc Business Logic
        df_results['Error_Actual_vs_Pred'] = df_results['SalePrice'] - df_results['Predicted_Price']
        df_results['Diff_Actual_vs_MMR'] = df_results['SalePrice'] - df_results['MarketPrice_MMR']
        
        conditions = [
            (df_results['Diff_Actual_vs_MMR'] > 500),
            (df_results['Diff_Actual_vs_MMR'] < -500)
        ]
        choices = ['Above Market (Profit)', 'Below Market (Loss)']
        df_results['Sales_Status'] = np.select(conditions, choices, default='Fair Market Price')

        # 4. Formatting
        print("   -> Formatting numeric precision...")
        money_cols = ['Predicted_Price', 'Forecast_1_Year', 'Forecast_3_Year',
                      'Error_Actual_vs_Pred', 'Diff_Actual_vs_MMR', 
                      'SalePrice', 'MarketPrice_MMR', 'CommissionEarned']
        
        for col in money_cols:
            if col in df_results.columns:
                df_results[col] = df_results[col].round(2)
        
        if 'Price_vs_MMR_Ratio' in df_results.columns:
            df_results['Price_vs_MMR_Ratio'] = df_results['Price_vs_MMR_Ratio'].round(3)
        if 'Depreciation_3Y_Pct' in df_results.columns:
            df_results['Depreciation_3Y_Pct'] = df_results['Depreciation_3Y_Pct'].round(1)
        if 'MilesPerYear' in df_results.columns:
            df_results['MilesPerYear'] = df_results['MilesPerYear'].round(1)
        if 'AvgMPG' in df_results.columns:
            df_results['AvgMPG'] = df_results['AvgMPG'].round(1)
        if 'Condition_Group' in df_results.columns:
             df_results['Condition_Group'] = df_results['Condition_Group'].astype(str).replace('nan', 'Average')

        # 5. Saving
        from config.paths import DASHBOARD_DIR
        
        output_file_dash = DASHBOARD_DIR / 'model_results_for_bi.csv'
        df_results.to_csv(output_file_dash, index=False, sep=';')
        print(f"   -> Saved to Dashboard: {output_file_dash}")
        
        output_file_data = BASE_DIR / 'data' / 'model_results_for_bi.csv'
        df_results.to_csv(output_file_data, index=False, sep=';')
        print(f"   -> Saved to Data backup: {output_file_data}")

        # Data Lake Backup
        try:
            from datalake.minio_setup import DataLakeManager
            print("   -> Uploading Final BI Data to MinIO (Data Lake)...")
            datalake = DataLakeManager()
            datalake.save_to_processed(df_results, "model_results_bi.csv")
        except Exception as e:
            print(f"   [WARN] Failed to upload to Data Lake: {e}")
        
        return df_results

def main():
    print("\n" + "="*60)
    print("[INFO] STARTING MODEL TRAINING PIPELINE")
    print("="*60)
    
    print("\n[PHASE 1] Loading Cached Data")
    cache_dir = PROCESSED_DATA_DIR / 'ml_cache'
    
    try:
        with open(cache_dir / 'X_train.pkl', 'rb') as f: X_train = pickle.load(f)
        with open(cache_dir / 'X_test.pkl', 'rb') as f: X_test = pickle.load(f)
        with open(cache_dir / 'y_train.pkl', 'rb') as f: y_train = pickle.load(f)
        with open(cache_dir / 'y_test.pkl', 'rb') as f: y_test = pickle.load(f)
        with open(cache_dir / 'df_full.pkl', 'rb') as f: df_full = pickle.load(f)
        with open(cache_dir / 'X_full_scaled.pkl', 'rb') as f: X_full_scaled = pickle.load(f)
        print("   -> Data loaded successfully from disk")
    except FileNotFoundError:
        print("   [ERROR] Cached data not found. Run feature engineering first!")
        return None

    trainer = ModelTrainer()
    
    # Phase 2: Train
    print("\n[PHASE 2] Model Training")
    trainer.train_random_forest(X_train, y_train)
    
    # Phase 3: Evaluate
    print("\n[PHASE 3] Model Evaluation")
    metrics, y_pred = trainer.evaluate_model(X_test, y_test)
    feature_importance = trainer.get_feature_importance(X_train.columns)
    trainer.save_model("random_forest")
    trainer.create_visualizations(y_test, y_pred, feature_importance)
    
    # Phase 4: Generate Output
    df_results = trainer.generate_prediction_dataset(df_full, X_full_scaled)
    
    print("\n" + "="*60)
    print("[SUCCESS] TRAINING PIPELINE COMPLETE")
    print(f"Final Model Accuracy (R2): {metrics['r2_score']*100:.2f}%")
    print("="*60 + "\n")
    
    return trainer, df_results

if __name__ == "__main__":
    main()