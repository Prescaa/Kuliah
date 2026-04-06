import os

# Mendapatkan jalur dasar proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jalur dataset disesuaikan dengan struktur: dataset/train/
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "train")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
CLASS_NAMES = ["Pensil", "Pulpen", "Spidol"]

# Definisi 3 Skenario Eksperimen untuk dijalankan secara batch
EXPERIMENTS = {
    "eksperimen_1": {
        "name": "Eksperimen 1 — Baseline SVM (RBF)",
        "algorithm": "svm",
        "kernel": "rbf",
        "C": 1.0,
        "gamma": "scale",
        "test_split": 0.2,
        "img_size": (128, 128)
    },
    "eksperimen_2": {
        "name": "Eksperimen 2 — Optimized SVM (High C)",
        "algorithm": "svm",
        "kernel": "rbf",
        "C": 10.0,   
        "gamma": 0.01,  
        "test_split": 0.2,
        "img_size": (128, 128)
    },
    "eksperimen_3": {
        "name": "Eksperimen 3 — Random Forest Ensemble",
        "algorithm": "rf",
        "n_estimators": 200,
        "test_split": 0.3,
        "img_size": (128, 128)
    }
}

os.makedirs(RESULTS_DIR, exist_ok=True)