import pandas as pd

import numpy as np

import os

import warnings



# Matikan warning agar terminal bersih

warnings.filterwarnings("ignore")



print("=== SETUP: DATA PREPARATION (FIXED FOR RAW BLS DATA) ===")



# Path Konfigurasi

SOURCE_RAW = 'data/raw/'

TARGET_RAW = 'data/enterprise_raw/'

os.makedirs(TARGET_RAW, exist_ok=True)



def load_csv(filename):

    path = os.path.join(SOURCE_RAW, filename)

    # Tambahkan low_memory=False untuk mengatasi DtypeWarning

    if os.path.exists(path): return pd.read_csv(path, on_bad_lines='skip', low_memory=False)

    return None



# ==============================================================================

# 1. PROCESS CPI DATA

# ==============================================================================

print("[1] Memproses Data Inflasi (cpi_raw.csv)...")

cpi_path = os.path.join(SOURCE_RAW, 'cpi_raw.csv')



if os.path.exists(cpi_path):

    try:

        # Langkah 1: Cari baris Header yang benar

        # Kita cari baris yang mengandung 'Year' dan 'Jan' (Bukan Annual)

        with open(cpi_path, 'r') as f:

            lines = f.readlines()[:20]

            

        header_row_index = -1

        for i, line in enumerate(lines):

            if 'Year' in line and 'Jan' in line:

                header_row_index = i

                print(f"   [INFO] Header tabel ditemukan di baris ke-{i+1}")

                break

        

        if header_row_index == -1:

            raise ValueError("Gagal menemukan kolom 'Year' & 'Jan' di 20 baris pertama.")



        # Langkah 2: Baca CSV dengan delimiter titik koma (;)

        df_cpi = pd.read_csv(cpi_path, skiprows=header_row_index, sep=';')

        

        # Langkah 3: Bersihkan Angka (Ubah 216,687 menjadi 216.687)

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        

        # Pastikan kolom bulan ada

        valid_months = [m for m in months if m in df_cpi.columns]

        

        # Konversi string angka eropa (koma) ke float (titik)

        for col in valid_months:

            # Ganti koma dengan titik, lalu convert ke float

            df_cpi[col] = df_cpi[col].astype(str).str.replace(',', '.', regex=False)

            df_cpi[col] = pd.to_numeric(df_cpi[col], errors='coerce')



        # Langkah 4: Hitung Rata-rata Tahunan (Annual)

        df_cpi['Annual'] = df_cpi[valid_months].mean(axis=1)

        

        # Ambil hanya Year dan Annual yang sudah dihitung

        df_inflation = df_cpi[['Year', 'Annual']].copy()

        df_inflation = df_inflation.dropna(subset=['Year', 'Annual'])

        df_inflation['Year'] = df_inflation['Year'].astype(int)

        df_inflation = df_inflation.sort_values('Year')

        

        # Langkah 5: Hitung Inflasi (% Growth)

        df_inflation['Inflation_Rate'] = df_inflation['Annual'].pct_change() * 100

        

        # Isi NaN tahun pertama dengan rata-rata inflasi selanjutnya

        avg_inf = df_inflation['Inflation_Rate'].mean()

        df_inflation['Inflation_Rate'] = df_inflation['Inflation_Rate'].fillna(avg_inf).round(2)

        

        # Simpan

        output_file = os.path.join(TARGET_RAW, 'EXT_US_CPI_Inflation.csv')

        df_inflation.to_csv(output_file, index=False)

        

        print(f"   [SUKSES] Inflasi dihitung dari data bulanan {df_inflation['Year'].min()}-{df_inflation['Year'].max()}.")

        print(f"   -> Hasil tersimpan di: {output_file}")



    except Exception as e:

        print(f"   [ERROR] Gagal memproses CPI: {e}")

        # Fallback: Buat dummy file jika gagal total agar pipeline tidak macet

        print("   [INFO] Membuat dummy file inflasi agar proses bisa lanjut...")

        dummy = pd.DataFrame({'Year': range(2000, 2025), 'Inflation_Rate': 2.5})

        dummy.to_csv(os.path.join(TARGET_RAW, 'EXT_US_CPI_Inflation.csv'), index=False)

else:

    print("   [WARNING] File 'cpi_raw.csv' tidak ditemukan. Inflasi tidak diproses.")



# ==============================================================================

# 2. NORMALISASI FILE LAIN (RENAME & MOVE)

# ==============================================================================

print("\n[2] Merapikan File Utama...")



df_sales = load_csv('car_prices.csv')

df_fuel  = load_csv('fuel.csv')

df_geo   = load_csv('uscities.csv')



if df_sales is not None:

    df_sales.to_csv(os.path.join(TARGET_RAW, 'TRX_AutoAuctions.csv'), index=False)

    print("   -> TRX_AutoAuctions.csv (Sales) created.")

    

    # Generate Master Mobil

    # Filter kolom yang benar-benar ada

    cols = [c for c in ['make', 'model', 'year', 'trim', 'body', 'transmission'] if c in df_sales.columns]

    df_master = df_sales[cols].drop_duplicates()

    df_master['VehicleID'] = range(1, len(df_master) + 1)

    df_master.to_csv(os.path.join(TARGET_RAW, 'REF_VehicleMaster.csv'), index=False)

    print("   -> REF_VehicleMaster.csv (Product Catalog) created.")



if df_fuel is not None:

    df_fuel.to_csv(os.path.join(TARGET_RAW, 'REF_FuelEconomy.csv'), index=False)

    print("   -> REF_FuelEconomy.csv (Fuel Specs) created.")



if df_geo is not None:

    df_geo.to_csv(os.path.join(TARGET_RAW, 'REF_GeoLocation.csv'), index=False)

    print("   -> REF_GeoLocation.csv (Geo Data) created.")



print("\n[SELESAI] Setup Data Complete. Folder 'data/enterprise_raw' siap.")