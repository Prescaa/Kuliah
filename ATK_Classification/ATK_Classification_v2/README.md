# ATK Classification (3 Kelas) — Panduan Penggunaan
**Rifky Putra Mahardika | NIM: 2310817210023**
**Program Studi: Teknologi Informasi | Mata Kuliah: Pembelajaran Mesin I**

---

## Struktur Project

```
ATK_Classification/
├── config.py          ← Edit di sini untuk ganti eksperimen / tambah kelas
├── train.py           ← Jalankan untuk training
├── evaluate.py        ← Jalankan untuk confusion matrix & laporan
├── predict.py         ← Prediksi gambar baru (bonus)
├── requirements.txt
├── README.md
├── dataset/
│   ├── pensil/
│   ├── pulpen/
│   └── spidol/
└── results/
    ├── eksperimen_1/
    ├── eksperimen_2/
    └── eksperimen_3/
```

---

## Info Dataset (3 Kelas)

| Kelas  | Foto Asli (estimasi) | Setelah Augmentasi  |
|--------|----------------------|---------------------|
| Pensil | 8-10 foto            | 72-90 gambar        |
| Pulpen | 8-10 foto            | 72-90 gambar        |
| Spidol | 8-10 foto            | 72-90 gambar        |
| Total  | 24-30 foto           | ~216-270 gambar     |

Rumus: (foto asli x jumlah teknik augmentasi) + foto asli = total per kelas

---

## Setup Awal (Lakukan Sekali)

### 1. Pastikan Python 3.9-3.11 terinstall
Download: https://www.python.org/downloads/

### 2. Buat & Aktifkan Virtual Environment
```
python -m venv venv
venv\Scripts\activate        (Windows)
source venv/bin/activate     (Mac/Linux)
```

### 3. Install Library
```
pip install -r requirements.txt
```

### 4. Siapkan Dataset
Susun seperti ini di dalam folder dataset/:
```
dataset/
├── pensil/
├── pulpen/
└── spidol/
```
Nama subfolder HARUS persis sama dengan CLASS_NAMES di config.py.

---

## Cara Menjalankan (3 Eksperimen)

Eksperimen 1: ACTIVE_EXPERIMENT = "eksperimen_1" -> python train.py -> python evaluate.py
Eksperimen 2: ACTIVE_EXPERIMENT = "eksperimen_2" -> python train.py -> python evaluate.py
Eksperimen 3: ACTIVE_EXPERIMENT = "eksperimen_3" -> python train.py -> python evaluate.py

---

## Ringkasan 3 Eksperimen

| Parameter          | Eks. 1        | Eks. 2                | Eks. 3            |
|--------------------|---------------|-----------------------|-------------------|
| Optimizer          | Adam          | Adam                  | SGD + Momentum    |
| Learning Rate      | 0.001         | 0.0001                | 0.01              |
| Batch Size         | 16            | 8                     | 16                |
| Epochs             | 30            | 50                    | 40                |
| Fine-Tune Backbone | Tidak         | Ya (dari layer 100)   | Tidak             |
| Dropout            | 0.3           | 0.4                   | 0.3               |
| Split Train/Val/Te | 80/10/10%     | 80/10/10%             | 70/15/15%         |

---

## Output per Eksperimen

```
results/eksperimen_X/
├── best_model.keras
├── training_log.csv
├── training_history.png
├── confusion_matrix.png
├── confusion_matrix_normalized.png
├── prediction_distribution.png
├── classification_report.txt
├── summary.json
├── X_test.npy
└── y_test.npy
```

---

## Prediksi Gambar Baru

python predict.py --image path/ke/foto.jpg
python predict.py --folder path/ke/folder/foto/

---

## Menambah Kelas Baru

1. Buat subfolder: dataset/penggaris/
2. Isi dengan foto
3. Edit config.py: CLASS_NAMES = ["pensil", "pulpen", "spidol", "penggaris"]
4. Jalankan ulang train.py

---

## Tips

- Overfitting (train acc >> val acc): kurangi epochs, naikkan dropout, tambah foto
- Underfitting (akurasi rendah): naikkan epochs, aktifkan fine-tuning (Eks. 2)
- Training lambat: gunakan GPU atau Google Colab
- Error memory: kurangi batch_size di config.py
