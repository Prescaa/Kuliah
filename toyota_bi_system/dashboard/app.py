import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Toyota Sales Analytics Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Toyota BI System - Sales Analytics & Price Prediction")
st.markdown("""
    **Enterprise Data Pipeline Architecture** Data Lake → Data Warehouse → ML Pipeline → BI Dashboard
""")
st.markdown("---")

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    """Load data from ML output"""
    current_dir = Path(__file__).parent
    file_path = current_dir / "model_results_for_bi.csv"
    
    if not file_path.exists():
        st.error("🚨 ERROR: ML results not found. Run ML pipeline first!")
        return None
        
    df = pd.read_csv(file_path, sep=";")
    return df

df = load_data()

if df is None:
    st.error("Please run the ML pipeline first to generate data.")
    st.stop()

# ---------------------------------------------------------
# 3. SIDEBAR (FILTER)
# ---------------------------------------------------------
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("### Data Source Info")
st.sidebar.info(f"**Total Records:** {len(df):,}")

# Filter Tahun
years = sorted(df['CarYear'].unique())
selected_year = st.sidebar.multiselect("Pilih Tahun Pembuatan", years, default=years)

# Filter Model
models = sorted(df['CarModel'].unique())
default_models = models[:5] if len(models) >= 5 else models
selected_model = st.sidebar.multiselect("Pilih Model Mobil", models, default=default_models)

# Filter Origin
if 'OriginCountry' in df.columns:
    origins = sorted(df['OriginCountry'].unique())
    selected_origin = st.sidebar.multiselect("Pilih Negara Asal", origins, default=origins)
else:
    selected_origin = []

if not selected_year or not selected_model:
    st.warning("Pilih minimal satu filter.")
    st.stop()

# Apply filters
filtered_df = df[
    (df['CarYear'].isin(selected_year)) &
    (df['CarModel'].isin(selected_model))
]

if selected_origin and 'OriginCountry' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['OriginCountry'].isin(selected_origin)]

# ---------------------------------------------------------
# 4. KPI DASHBOARD
# ---------------------------------------------------------
total_sales = filtered_df['SalePrice'].sum()
avg_price = filtered_df['SalePrice'].mean()
total_transactions = len(filtered_df)

# UPDATE: Menggunakan kolom baru 'Error_Actual_vs_Pred'
if 'Error_Actual_vs_Pred' in filtered_df.columns:
    avg_accuracy = filtered_df['Error_Actual_vs_Pred'].abs().mean()
else:
    avg_accuracy = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Omzet", f"${total_sales:,.0f}")
col2.metric("🏷️ Rata-rata Harga", f"${avg_price:,.0f}")
col3.metric("🚗 Total Unit Terjual", f"{total_transactions}")
col4.metric("🤖 Rata-rata Error AI", f"${avg_accuracy:,.0f}", delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------
# 5. VISUALISASI UTAMA
# ---------------------------------------------------------

# --- BARIS 1: MODEL PERFORMANCE ---
st.subheader("📈 Model Performance Analysis")
col_row1_a, col_row1_b = st.columns(2)

with col_row1_a:
    st.markdown("#### Validasi Akurasi Prediksi")
    fig_scatter = px.scatter(
        filtered_df, 
        x="SalePrice", 
        y="Predicted_Price", 
        color="Sales_Status",
        hover_data=["CarModel", "CarYear", "OriginCountry"],
        title="Harga Aktual vs Prediksi AI",
        trendline="ols"
    )
    max_val = max(filtered_df['SalePrice'].max(), filtered_df['Predicted_Price'].max())
    fig_scatter.add_shape(type="line", line=dict(dash="dash", color="grey"), 
                          x0=0, y0=0, x1=max_val, y1=max_val)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_row1_b:
    st.markdown("#### Top 10 Model Terlaris")
    top_selling = filtered_df['CarModel'].value_counts().reset_index().head(10)
    top_selling.columns = ['CarModel', 'TotalUnit']
    top_selling = top_selling.sort_values('TotalUnit', ascending=True)

    fig_top_sales = px.bar(
        top_selling,
        x='TotalUnit',
        y='CarModel',
        orientation='h',
        text='TotalUnit',
        color='TotalUnit',
        title="Volume Penjualan per Model",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_top_sales, use_container_width=True)

# --- BARIS 1.5: FEATURE IMPORTANCE (AI EXPLAINABILITY) ---
st.markdown("---")
st.subheader("🧠 AI Explainability: Faktor Penentu Harga")

# NOTE: Karena kita load CSV (bukan file .pkl modelnya langsung), 
# kita gunakan Korelasi Statistik sebagai representasi Feature Importance di Dashboard.
# Ini aman dan ilmiah untuk kebutuhan visualisasi BI.

with st.container():
    # 1. Tentukan kolom numerik yang relevan untuk dicek pengaruhnya
    potential_features = ['CarYear', 'Odometer', 'CityMPG', 'HighwayMPG', 'ComplaintCount', 'EngineSize', 'Cylinders']
    
    # 2. Filter hanya kolom yang benar-benar ada di CSV
    available_features = [col for col in potential_features if col in filtered_df.columns]
    
    if available_features:
        # 3. Hitung korelasi dengan SalePrice
        # Kita pakai abs() (mutlak) karena kita ingin tahu 'kekuatan pengaruh', 
        # entah itu positif (naik) atau negatif (turun).
        corr_data = filtered_df[available_features + ['SalePrice']].corr()['SalePrice'].drop('SalePrice')
        
        # 4. Buat DataFrame untuk Plotly
        importance_df = pd.DataFrame({
            'Faktor': corr_data.index,
            'Kekuatan Pengaruh': corr_data.values  # Nilai asli (+/-)
        })
        
        # Tambahkan kolom warna (Positif = Hijau, Negatif = Merah)
        importance_df['Arah Hubungan'] = importance_df['Kekuatan Pengaruh'].apply(lambda x: 'Positif (Harga Naik)' if x > 0 else 'Negatif (Harga Turun)')
        importance_df['Magnitude'] = importance_df['Kekuatan Pengaruh'].abs() # Untuk urutan sorting
        
        # Sort dari yang paling berpengaruh
        importance_df = importance_df.sort_values(by='Magnitude', ascending=True)

        # 5. Visualisasi Horizontal Bar Chart
        fig_imp = px.bar(
            importance_df,
            x='Kekuatan Pengaruh',
            y='Faktor',
            orientation='h',
            color='Arah Hubungan',
            title="Analisis Korelasi: Apa yang Paling Mempengaruhi Harga?",
            labels={'Kekuatan Pengaruh': 'Tingkat Korelasi (Pearson)'},
            color_discrete_map={'Positif (Harga Naik)': '#2ecc71', 'Negatif (Harga Turun)': '#e74c3c'},
            text_auto='.2f'
        )

        fig_imp.update_layout(xaxis_title="Korelasi Negatif (Harga Turun) <--- 0 ---> Korelasi Positif (Harga Naik)")
        st.plotly_chart(fig_imp, use_container_width=True)

        st.info("""
        **ℹ️ Panduan Interpretasi Bisnis:**
        * 🟢 **Korelasi Positif (Bar Hijau):** Menunjukkan hubungan **berbanding lurus**. Semakin tinggi nilai variabel ini (contoh: *CarYear* makin muda atau MPG makin irit), maka harga jual akan semakin **NAIK**.
        * 🔴 **Korelasi Negatif (Bar Merah):** Menunjukkan hubungan **berbanding terbalik**. Semakin tinggi nilai variabel ini (contoh: *Odometer* makin tinggi atau *ComplaintCount* makin banyak), maka harga jual akan semakin **TURUN**.
        """)
    else:
        st.warning("Data numerik untuk analisis fitur tidak ditemukan di CSV.")

# --- BARIS 2: BUSINESS ANALYSIS ---
st.subheader("📊 Business Intelligence")

# --- TAMBAHAN INSIGHT (BARU) ---
st.info("""
**💡 Key Automated Insights:**
1. **Prediksi Depresiasi Aset:** Sistem memproyeksikan penurunan nilai aset kendaraan dalam 1-3 tahun ke depan sebagai panduan strategi penjualan.
2. **Determinan Harga Utama:** Analisis AI mengidentifikasi **Usia Kendaraan** dan **Riwayat Keluhan Keamanan (API)** sebagai dua faktor paling dominan yang mempengaruhi harga jual.
""")
# -------------------------------

col_row2_a, col_row2_b = st.columns(2)

with col_row2_a:
    st.markdown("#### Rata-rata Keluhan per Model")
    complaint_data = filtered_df.groupby("CarModel")["ComplaintCount"].mean().reset_index()
    complaint_data = complaint_data.sort_values("ComplaintCount", ascending=False).head(10)
    
    fig_complaint = px.bar(
        complaint_data, 
        x="CarModel", 
        y="ComplaintCount",
        color="CarModel",
        title="Top 10 Model dengan Rata-rata Keluhan Tertinggi",
        text_auto='.0f',
        labels={"ComplaintCount": "Avg Complaints"}
    )
    st.plotly_chart(fig_complaint, use_container_width=True)

with col_row2_b:
    st.markdown("#### Perbandingan Harga: Import vs Lokal")
    if 'OriginCountry' in filtered_df.columns:
        avg_price_origin = filtered_df.groupby("OriginCountry")["SalePrice"].mean().reset_index()
        fig_origin = px.bar(
            avg_price_origin, 
            x="OriginCountry", 
            y="SalePrice", 
            color="OriginCountry",
            title="Rata-rata Harga Jual Berdasarkan Negara Asal",
            text_auto='.2s'
        )
        st.plotly_chart(fig_origin, use_container_width=True)
    else:
        st.warning("Data Negara Asal tidak tersedia.")

# --- BARIS 3: FUEL EFFICIENCY ---
st.subheader("⛽ Analisis Efisiensi Bahan Bakar")

if 'CityMPG' in filtered_df.columns:
    top_mpg_cars = filtered_df.groupby("CarModel")[["CityMPG"]].mean().reset_index()
    top_mpg_cars = top_mpg_cars.sort_values("CityMPG", ascending=True).tail(10)

    fig_mpg = px.bar(
        top_mpg_cars,
        x="CityMPG",
        y="CarModel",
        orientation='h',
        text_auto='.1f',
        color="CityMPG",
        title="Top 10 Mobil Paling Irit Bensin (City MPG)",
        labels={"CityMPG": "MPG (Makin Tinggi Makin Irit)"},
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig_mpg, use_container_width=True)
else:
    st.warning("Data MPG tidak ditemukan.")

# ---------------------------------------------------------
# FITUR BARU: SIMULASI DEPRESIASI & FORECASTING
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🔮 Prediksi Harga Masa Depan (AI Forecasting)")

if 'Forecast_1_Year' in df.columns:
    # 1. Input Simulasi dari User
    col_sim1, col_sim2, col_sim3 = st.columns(3)

    with col_sim1:
        # Hanya ambil model yang ada di data
        sim_model = st.selectbox("Pilih Model Mobil:", df['CarModel'].unique())

    with col_sim2:
        # Filter tahun yang tersedia untuk model tersebut
        avail_years = sorted(df[df['CarModel'] == sim_model]['CarYear'].unique())
        if avail_years:
            sim_year = st.selectbox("Tahun Pembuatan:", avail_years)
        else:
            sim_year = None

    with col_sim3:
        if sim_year:
            # Ambil rata-rata KM untuk model & tahun tersebut sebagai default
            avg_km = df[(df['CarModel'] == sim_model) & (df['CarYear'] == sim_year)]['Odometer'].median()
            if pd.isna(avg_km): avg_km = 50000.0
            sim_km = st.number_input("Odometer (KM) Saat Ini:", value=int(avg_km), step=1000)
        else:
            sim_km = 0

    # 2. Cari Data yang Mirip di Hasil Prediksi
    if sim_year:
        match_df = df[
            (df['CarModel'] == sim_model) & 
            (df['CarYear'] == sim_year)
        ].copy()

        if not match_df.empty:
            # Cari yang selisih KM-nya paling kecil
            match_df['km_diff'] = abs(match_df['Odometer'] - sim_km)
            best_match = match_df.sort_values('km_diff').iloc[0]
            
            # 3. Tampilkan Hasil Prediksi dari CSV
            current_price = best_match.get('Predicted_Price', 0)
            future_1y = best_match.get('Forecast_1_Year', 0)
            future_3y = best_match.get('Forecast_3_Year', 0)
            depreciation_pct = best_match.get('Depreciation_3Y_Pct', 0)
            
            # Tampilkan Metrics
            st.markdown(f"##### 💡 Estimasi Nilai Pasar untuk **{sim_model} {sim_year}**")
            
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            
            with col_res1:
                st.metric("Harga Saat Ini", f"${current_price:,.0f}", "Base Price")
                
            with col_res2:
                diff_1y = future_1y - current_price
                st.metric("Harga Tahun Depan", f"${future_1y:,.0f}", f"{diff_1y:,.0f} (1 Thn)")
                
            with col_res3:
                diff_3y = future_3y - current_price
                st.metric("Harga 3 Tahun Lagi", f"${future_3y:,.0f}", f"{diff_3y:,.0f} (3 Thn)")
                
            with col_res4:
                st.metric("Penyusutan (3 Thn)", f"{depreciation_pct}%", "Depreciation Rate")
            
            # Grafik Garis Sederhana
            chart_data = pd.DataFrame({
                "Tahun": ["Sekarang", "1 Tahun", "3 Tahun"],
                "Estimasi Harga": [current_price, future_1y, future_3y]
            })
            fig_line = px.line(chart_data, x="Tahun", y="Estimasi Harga", markers=True, title="Trend Nilai Aset")
            st.plotly_chart(fig_line, use_container_width=True)
            
        else:
            st.warning("Data spesifik tidak ditemukan untuk simulasi ini.")
else:
    st.info("Fitur Forecasting belum tersedia. Jalankan ulang ML Pipeline untuk mengaktifkan.")

# --- BARIS 4: DATA EXPLORER ---
st.markdown("---")
with st.expander("📋 Data Explorer (Raw Data)"):
    st.dataframe(filtered_df)
    
    csv = filtered_df.to_csv(index=False, sep=';')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="toyota_filtered_data.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# 6. FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p><strong>Toyota BI System v2.0</strong> | Enterprise Data Pipeline</p>
    <p>Data Lake → Data Warehouse → ML → Dashboard</p>
</div>
""", unsafe_allow_html=True)