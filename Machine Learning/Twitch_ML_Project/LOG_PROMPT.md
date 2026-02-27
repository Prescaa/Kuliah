# LOG PROMPT PENGEMBANGAN MODEL PREDIKSI TWITCH (2016-2024)

Jadi di dalam dokumen ini terdapat rangkaian logika yang dipakai selama proses pembangunan model regresi linear teroptimasi untuk memprediksi popularitas game di twitch.

# 1. LOAD & EXPLORE DATASET

import pandas as pd
import numpy as np

try:
    df_game = pd.read_csv('data/Twitch_game_data.csv', encoding='latin1')
except:
    df_game = pd.read_csv('data/Twitch_game_data.csv', encoding='cp1252')

print(df_game.describe())
print(df_game.isnull().sum())

# 2. HYBRID TARGET TRANSFORMATION

### Transformasi target ke skala logaritmik
y_original = df_game['Hours_watched']
y_log = np.log1p(y_original)

### Fungsi untuk mengembalikan ke skala asli saat evaluasi
def inverse_target(y_log_val):
    return np.expm1(y_log_val)

# 3. FEATURE ENGINEERING (CYCLICAL & ERA)

### Cyclical Month Encoding
df_game['month_sin'] = np.sin(2 * np.pi * df_game['Month']/12)
df_game['month_cos'] = np.cos(2 * np.pi * df_game['Month']/12)

### Era Encoding (Pra-Pandemi vs Era Modern)
df_game['era_enc'] = df_game['Year'].apply(lambda x: 0 if x < 2020 else (1 if x < 2022 else 2))

# 4. HYBRID EXPERIMENT RUNNER

def run_hybrid_exp(name, model, X_train, X_test, y_train_log, y_test_log):
    # Training pada skala LOG
    model.fit(X_train, y_train_log)
    y_pred_log = model.predict(X_test)
    
    # Inversi ke SKALA ASLI untuk metrik error
    y_pred_orig = np.expm1(y_pred_log)
    y_test_orig = np.expm1(y_test_log)
    
    # Hitung metrik
    mae = mean_absolute_error(y_test_orig, y_pred_orig)
    mape = np.mean(np.abs((y_test_orig - y_pred_orig) / y_test_orig)) * 100
    r2 = model.score(X_test, y_test_log)
    
    return {"Model": name, "MAE": mae, "MAPE": mape, "R2": r2}

# 5. ENHANCED MODEL: RIDGE + POLY

from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline

model_poly_ridge = Pipeline([
    ("poly", PolynomialFeatures(degree=2)),
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=50.0))
])

### Eksperimen model terbaik
res_poly = run_hybrid_exp("Ridge + Poly", model_poly_ridge, X_train, X_test, y_train_log, y_test_log)

# 6. STRESS TEST & LOGGING

noise_levels = [0, 0.05, 0.1, 0.3]
for sigma in noise_levels:
    X_test_noise = X_test + np.random.normal(0, sigma * X_test.std(), X_test.shape)
    score = model_baseline.score(X_test_noise, y_test_log)
    print(f"Noise sigma={sigma}: R2={score}")

### Simpan semua hasil ke DataFrame untuk Experiment Log
log_df = pd.DataFrame(experiments)
print(log_df.to_string(index=False))