# Membangun dan Membandingkan Model Regresi Linear Teroptimasi dalam Analisis Prediksi Popularitas Game pada Platform Twitch 2016–2024 [cite: 1]

**Disusun oleh:** [cite: 2]
* Akmallullail Sya’ban (2310817310010) [cite: 3]
* Rifky Putra Mahardika (2310817210023) [cite: 3]
* Allano Lintang Ertantora (2310817210004) [cite: 3]

## Ringkasan
Proyek ini membandingkan berbagai model regresi linear untuk memprediksi variabel `Hours_watched` (jumlah jam ditonton) dari dataset "Evolution of Top Games on Twitch" periode 2016–2024[cite: 10, 15]. Kami mengevaluasi performa model:
1. **LinearRegression (Baseline)**: Sebagai model dasar tanpa regularisasi[cite: 25].
2. **Ridge & Lasso Regression**: Untuk menangani multikolinearitas melalui regularisasi L1/L2[cite: 25, 44].
3. **Ridge + Polynomial Interaction**: Model terbaik yang menangkap hubungan non-linear antar fitur[cite: 25, 43].

Evaluasi dilakukan menggunakan **5-Fold Cross Validation** dengan metrik MAE, RMSE, MAPE, dan R² yang dikembalikan ke skala asli untuk interpretasi bisnis[cite: 23, 24, 38].

## Struktur Proyek
* `main.py`: Skrip utama untuk proses training, evaluasi, logging hasil eksperimen, dan stress test[cite: 34].
* `visualization.py`: Skrip untuk menghasilkan visualisasi analisis (Actual vs Predicted, Heatmap, dan Top 10 Games).
* `src/`: Folder berisi modul modular `preprocessing.py` (pembersihan data) dan `model.py` (definisi arsitektur model)[cite: 40].
* `data/Twitch_game_data.csv`: Dataset input berisi performa 200 game teratas[cite: 11, 13].
* `LOG_PROMPT.md`: Dokumentasi interaksi pengembangan kodingan bersama AI.

## Dataset dan Target
* **Dataset**: Mencakup 21.000 baris data dengan 2.359 judul game unik[cite: 13].
* **Fitur (X)**: Rank, Game (Frequency Encoded), Month (Sin/Cos), Year, Hours_streamed, Peak_viewers, Streamers, Era_enc, dll[cite: 15, 40].
* **Target (y)**: `Hours_watched` (menggunakan Hybrid Log-Transformation untuk menangani skewness)[cite: 15, 21].

## Metodologi
1. **Pembersihan & Transformasi**: Menghapus data kosong, melakukan outlier handling berbasis 2.5x IQR pada skala log, dan mentransformasi target ke skala logaritma[cite: 21].
2. **Encoding**: Menggunakan *Frequency Encoding* untuk kategori Game dan *Cyclical Encoding* untuk fitur Month guna menangkap siklus tahunan[cite: 21, 40].
3. **Optimasi**: Implementasi *Polynomial Interaction* derajat 2 dan regularisasi Ridge ($\alpha=50$) untuk menangkap interaksi antar variabel[cite: 25, 44].
4. **Stress Test**: Menguji ketahanan model dengan menginjeksi *Gaussian Noise* ($\sigma=0.05$ hingga $0.30$) pada data input[cite: 58, 60].

## Hasil Eksperimen
Berdasarkan log eksperimen akhir: [cite: 25]
* **Model Terbaik**: Ridge + Polynomial Interaction menunjukkan R² tertinggi (0.93) dan MAPE terendah (31.13%)[cite: 25, 31].
* **Generalisasi**: Validasi K-Fold menunjukkan stabilitas model dengan skor R² rata-rata 0.9006[cite: 55].
* **Ketangguhan**: Pada kondisi Stress Test $\sigma=0.30$, model tetap *robust* dengan skor R² 0.8389[cite: 61, 68].

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