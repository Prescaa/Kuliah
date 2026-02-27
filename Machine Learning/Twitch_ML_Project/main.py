import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from src.preprocessing import Preprocessor
from src.model import ModelFactory
from src.evaluation import Evaluator

warnings.filterwarnings('ignore')

print("=== LOADING TWITCH DATASET (HYBRID MODE) ===")
try:
    df_game = pd.read_csv('data/Twitch_game_data.csv', encoding='latin1')
    df_global = pd.read_csv('data/Twitch_global_data.csv', encoding='latin1')
except:
    df_game = pd.read_csv('data/Twitch_game_data.csv', encoding='cp1252')
    df_global = pd.read_csv('data/Twitch_global_data.csv', encoding='cp1252')

print(f"Game data shape: {df_game.shape}")
print(f"Global data shape: {df_global.shape}")
print(f"Kolom: {df_game.columns.tolist()}")
print(f"\nMissing values:\n{df_game.isnull().sum()}")
print(f"Unique games: {df_game['Game'].nunique()}")
print(f"Tahun: {sorted(df_game['Year'].unique())}")

print("\nStatistik deskriptif:")
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(df_game.describe())

print("\n=== FEATURE ENGINEERING ===")
prep = Preprocessor()
df_game = prep.clean_data(df_game)
df_game = prep.feature_engineering(df_game)
print(f"Shape after feature engineering: {df_game.shape}")
print(f"Kolom baru: efficiency_ratio, viewer_per_channel, game_popularity_enc, month_sin, month_cos, era_enc")

print("\n=== PREPROCESSING ===")
print(f"Rows setelah drop missing Game: {len(df_game)}")
df_clean = prep.remove_outliers(df_game, 'Hours_watched')
print(f"Shape setelah outlier removal (2.5xIQR): {df_clean.shape}")

features = ['Rank', 'Year', 'Hours_streamed', 'Peak_viewers', 'game_popularity_enc', 'month_sin', 'month_cos', 'era_enc']
X = df_clean[features]
y_original = df_clean['Hours_watched']
y_log = prep.transform_target(y_original)

print(f"Target range (Original): {int(y_original.min())} - {int(y_original.max())}")

X_train, X_test, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)

experiments = []

def run_hybrid_exp(name, model):
    model.fit(X_train, y_train_log)
    y_pred_log = model.predict(X_test)
    
    y_pred_orig = prep.inverse_target(y_pred_log)
    y_test_orig = prep.inverse_target(y_test_log)
    
    res = Evaluator.get_all_metrics(y_test_orig, y_pred_orig)
    res['R2'] = model.score(X_test, y_test_log)
    
    experiments.append({"Model": name, **res})
    print(f"{name}\n  MAE={res['MAE']:.0f}  MAPE={res['MAPE']:.2f}%  R²={res['R2']:.4f}")

print("\n=== MODEL 1: BASELINE ===")
run_hybrid_exp("LR Baseline", ModelFactory.get_baseline())

print("\n=== MODEL 2: ENHANCED MODELS ===")
run_hybrid_exp("Ridge alpha=1.0", ModelFactory.get_ridge(alpha=1.0))
run_hybrid_exp("Ridge alpha=10.0", ModelFactory.get_ridge(alpha=10.0))
run_hybrid_exp("Lasso alpha=0.01", ModelFactory.get_lasso(alpha=0.01))
run_hybrid_exp("Ridge alpha=50.0 + Poly", ModelFactory.get_poly_ridge(degree=2, alpha=50.0))

print("\n=== STRESS TEST (Log Scale Stability) ===")
noise_levels = [0, 0.05, 0.1, 0.3]
for sigma in noise_levels:
    X_test_noise = X_test + np.random.normal(0, sigma * X_test.std(), X_test.shape)
    score = ModelFactory.get_baseline().fit(X_train, y_train_log).score(X_test_noise, y_test_log)
    print(f"  Noise sigma={sigma}: R²={score:.4f}")

print("\n=== EXPERIMENT LOG ===")
log_df = pd.DataFrame(experiments)
print(log_df.to_string(index=False))

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(ModelFactory.get_ridge(), X, y_log, cv=kf)

print("\n======================================================================")
print("FINAL SUMMARY")
best = log_df.loc[log_df['R2'].idxmax()]
print(f"Baseline: MAE={experiments[0]['MAE']:.0f} | R²={experiments[0]['R2']:.3f}")
print(f"Best:     MAE={best['MAE']:.0f} | MAPE={best['MAPE']:.2f}% | R²={best['R2']:.4f}")
print(f"Validasi K-Fold (Mean R2 Log-Scale): {cv_scores.mean():.4f}")
print("======================================================================")