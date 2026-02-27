# Membandingkan Model Regresi Linear dalam Analisis Prediksi Popularitas Game pada Platform Twitch 2016–2024

**Disusun oleh:**
* Akmallullail Sya’ban (2310817310010)
* Rifky Putra Mahardika (2310817210023) 
* Allano Lintang Ertantora (2310817210004) 

## Ringkasan
Proyek ini membandingkan berbagai model regresi linear untuk memprediksi variabel `Hours_watched` (jumlah jam ditonton) dari dataset "Evolution of Top Games on Twitch" periode 2016–2024. Kami mengevaluasi performa model:
1. **LinearRegression (Baseline)**: Sebagai model dasar tanpa regularisasi.
2. **Ridge & Lasso Regression**: Untuk menangani multikolinearitas melalui regularisasi L1/L2.
3. **Ridge + Polynomial Interaction**: Model terbaik yang menangkap hubungan non-linear antar fitur.

Evaluasi dilakukan menggunakan **5-Fold Cross Validation** dengan metrik MAE, RMSE, MAPE, dan R² yang dikembalikan ke skala asli untuk interpretasi bisnis.

## Struktur Proyek
* `main.py`: Skrip utama untuk proses training, evaluasi, logging hasil eksperimen, dan stress test.
* `visualization.py`: Skrip untuk menghasilkan visualisasi analisis (Actual vs Predicted, Heatmap, dan Top 10 Games).
* `src/`: Folder berisi modul modular `preprocessing.py` (pembersihan data) dan `model.py` (definisi arsitektur model).
* `data/Twitch_game_data.csv`: Dataset input berisi performa 200 game teratas.
* `LOG_PROMPT.md`: Dokumentasi interaksi pengembangan kodingan bersama AI.

## Dataset dan Target
* **Dataset**: Mencakup 21.000 baris data dengan 2.359 judul game unik.
* **Fitur (X)**: Rank, Game (Frequency Encoded), Month (Sin/Cos), Year, Hours_streamed, Peak_viewers, Streamers, Era_enc, dll.
* **Target (y)**: `Hours_watched` (menggunakan Hybrid Log-Transformation untuk menangani skewness).

## Metodologi
1. **Pembersihan & Transformasi**: Menghapus data kosong, melakukan outlier handling berbasis 2.5x IQR pada skala log, dan mentransformasi target ke skala logaritma.
2. **Encoding**: Menggunakan *Frequency Encoding* untuk kategori Game dan *Cyclical Encoding* untuk fitur Month guna menangkap siklus tahunan.
3. **Optimasi**: Implementasi *Polynomial Interaction* derajat 2 dan regularisasi Ridge ($\alpha=50$) untuk menangkap interaksi antar variabel.
4. **Stress Test**: Menguji ketahanan model dengan menginjeksi *Gaussian Noise* ($\sigma=0.05$ hingga $0.30$) pada data input.

## Hasil Eksperimen
Berdasarkan log eksperimen akhir:
* **Model Terbaik**: Ridge + Polynomial Interaction menunjukkan R² tertinggi (0.93) dan MAPE terendah (31.13%).
* **Generalisasi**: Validasi K-Fold menunjukkan stabilitas model dengan skor R² rata-rata 0.9006.
* **Ketangguhan**: Pada kondisi Stress Test $\sigma=0.30$, model tetap *robust* dengan skor R² 0.8389.

## Kebutuhan Environment
Gunakan Python 3.9+ dengan library berikut:
* `pandas`
* `numpy`
* `scikit-learn`
* `matplotlib`
* `seaborn`

## Cara Menjalankan
1. Pastikan dataset berada di folder `data/Twitch_game_data.csv`.
2. Jalankan perintah training:
   ```bash
   python main.py