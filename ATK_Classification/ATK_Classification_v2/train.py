import os
import time
import numpy as np
import joblib
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage.io import imread
from skimage.transform import resize
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from config import EXPERIMENTS, DATASET_DIR, CLASS_NAMES, RESULTS_DIR

def extract_features(image_path, size):
    img = imread(image_path, as_gray=True)
    img_res = resize(img, size)
    # Menggunakan orientasi 11 untuk detail geometri objek yang lebih tajam
    fd = hog(img_res, orientations=11, pixels_per_cell=(8, 8), 
             cells_per_block=(2, 2), visualize=False)
    return fd

def run_experiment(exp_id, cfg):
    print(f"\n{'='*60}")
    print(f"  MENJALANKAN: {cfg['name']}")
    print(f"{'='*60}")
    
    output_dir = os.path.join(RESULTS_DIR, exp_id)
    os.makedirs(output_dir, exist_ok=True)

    X, y = [], []
    for idx, cls in enumerate(CLASS_NAMES):
        cls_path = os.path.join(DATASET_DIR, cls)
        if not os.path.exists(cls_path):
            print(f"  [ERROR] Folder tidak ditemukan: {cls_path}")
            continue
            
        count = 0
        for img_name in os.listdir(cls_path):
            if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                feat = extract_features(os.path.join(cls_path, img_name), cfg['img_size'])
                X.append(feat)
                y.append(idx)
                count += 1
        print(f"  [DONE] Kelas {cls:8}: {count} gambar diproses.")
    
    if len(X) == 0:
        print("  [ERROR] Tidak ada data untuk diproses. Cek jalur dataset Anda.")
        return 0

    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg['test_split'], stratify=y, random_state=42
    )

    start_time = time.time()
    if cfg['algorithm'] == 'svm':
        model = SVC(kernel=cfg['kernel'], C=cfg['C'], gamma=cfg.get('gamma', 'scale'), probability=True)
    else:
        model = RandomForestClassifier(n_estimators=cfg['n_estimators'], random_state=42)

    model.fit(X_train, y_train)
    duration = time.time() - start_time
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # Simpan model dan data uji untuk keperluan evaluasi
    joblib.dump(model, os.path.join(output_dir, "model_ml1.pkl"))
    np.save(os.path.join(output_dir, "X_test.npy"), X_test)
    np.save(os.path.join(output_dir, "y_test.npy"), y_test)
    
    print(f"  [INFO] Selesai dalam {duration:.2f} detik.")
    print(f"  > Akurasi: {acc*100:.2f}%")
    
    return acc * 100

def visualize_results(results):
    names = list(results.keys())
    accuracies = list(results.values())
    
    plt.figure(figsize=(10, 6))
    colors = ['#aec6cf', '#ffb347', '#77dd77']
    bars = plt.bar(names, accuracies, color=colors, edgecolor='black', alpha=0.8)
    
    plt.axhline(y=80, color='red', linestyle='--', label='Target Akurasi (80%)')
    plt.ylim(0, 100)
    plt.ylabel('Akurasi (%)', fontweight='bold')
    plt.title('Perbandingan Akurasi Eksperimen Klasifikasi ATK', fontsize=14)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.2f}%", 
                 ha='center', va='bottom', fontweight='bold')

    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "perbandingan_akurasi.png"))
    plt.show()

if __name__ == "__main__":
    all_results = {}
    for exp_id, cfg in EXPERIMENTS.items():
        accuracy = run_experiment(exp_id, cfg)
        if accuracy > 0:
            label = "SVM Baseline" if exp_id == "eksperimen_1" else \
                    "SVM Optimized" if exp_id == "eksperimen_2" else "Random Forest"
            all_results[label] = accuracy
    
    if all_results:
        visualize_results(all_results)