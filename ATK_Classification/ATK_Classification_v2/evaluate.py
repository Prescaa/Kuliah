import os
import random
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.feature import hog
from skimage.io import imread
from skimage.transform import resize
from sklearn.metrics import classification_report, confusion_matrix
from config import EXPERIMENTS, CLASS_NAMES, RESULTS_DIR, DATASET_DIR

# --- FUNGSI PEMBANTU UNTUK VISUALISASI SAMPEL ---
def extract_single_image(image_path, size=(128, 128)):
    """Fungsi untuk ekstraksi fitur HOG pada satu gambar contoh."""
    img = imread(image_path, as_gray=True)
    img_res = resize(img, size)
    fd = hog(img_res, orientations=11, pixels_per_cell=(8, 8), 
             cells_per_block=(2, 2), visualize=False)
    return fd, img_res

def visualize_samples(model, cfg, exp_dir):
    """Mengambil satu sampel acak dari setiap kelas dan menampilkan hasil prediksinya."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Visualisasi Sampel Prediksi - {cfg['name']}", fontsize=14, fontweight='bold')

    for i, cls in enumerate(CLASS_NAMES):
        # Akses folder kelas di dataset/train/
        cls_folder = os.path.join(DATASET_DIR, cls)
        if not os.path.exists(cls_folder):
            continue
            
        all_images = [f for f in os.listdir(cls_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not all_images:
            continue
            
        # Ambil gambar acak
        random_img_name = random.choice(all_images)
        img_path = os.path.join(cls_folder, random_img_name)
        
        # Ekstraksi dan Prediksi
        features, img_display = extract_single_image(img_path)
        prediction = model.predict([features])[0]
        prob = model.predict_proba([features])[0]
        
        label_pred = CLASS_NAMES[prediction]
        confidence = prob[prediction] * 100
        
        # Tampilkan di plot
        axes[i].imshow(img_display, cmap='gray')
        # Warna teks hijau jika benar (prediksi sesuai folder), merah jika salah
        color = 'green' if label_pred == cls else 'red'
        
        axes[i].set_title(f"Asli: {cls}\nPrediksi: {label_pred}\nConf: {confidence:.2f}%", 
                          color=color, fontsize=10, fontweight='bold')
        axes[i].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(exp_dir, "sample_predictions.png"))
    plt.close()

# --- FUNGSI CONFUSION MATRIX ---
def plot_confusion_matrix(y_true, y_pred, exp_name, output_dir, normalize=False):
    cm = confusion_matrix(y_true, y_pred)
    fmt = ".2f" if normalize else "d"
    title = "Confusion Matrix (Normalized)" if normalize else "Confusion Matrix"
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt=fmt, cmap="YlGnBu", 
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title(f"{title}\n{exp_name}")
    plt.ylabel('Label Asli')
    plt.xlabel('Label Prediksi')
    
    fname = "cm_normalized.png" if normalize else "cm_standard.png"
    plt.savefig(os.path.join(output_dir, fname))
    plt.close()

# --- MAIN EVALUATION ---
def main():
    print(f"\n{'='*60}")
    print("  MENJALANKAN EVALUASI MODEL")
    print(f"{'='*60}")

    for exp_id, cfg in EXPERIMENTS.items():
        exp_dir = os.path.join(RESULTS_DIR, exp_id)
        model_path = os.path.join(exp_dir, "model_ml1.pkl")
        
        if not os.path.exists(model_path):
            print(f"  [SKIP] Model untuk {exp_id} tidak ditemukan. Jalankan train.py dulu.")
            continue

        print(f"\nMengevaluasi: {cfg['name']}...")
        model = joblib.load(model_path)
        X_test = np.load(os.path.join(exp_dir, "X_test.npy"))
        y_test = np.load(os.path.join(exp_dir, "y_test.npy"))

        # 1. Jalankan Prediksi pada Data Uji
        y_pred = model.predict(X_test)
        
        # 2. Simpan Laporan Klasifikasi (Precision, Recall, F1)
        report = classification_report(y_test, y_pred, target_names=CLASS_NAMES)
        with open(os.path.join(exp_dir, "report_evaluasi.txt"), "w") as f:
            f.write(f"Hasil Evaluasi: {cfg['name']}\n")
            f.write("="*30 + "\n")
            f.write(report)
        
        # 3. Generate Confusion Matrix
        plot_confusion_matrix(y_test, y_pred, cfg['name'], exp_dir, normalize=False)
        plot_confusion_matrix(y_test, y_pred, cfg['name'], exp_dir, normalize=True)
        
        # 4. TAMBAHAN: Visualisasi Sampel Prediksi
        visualize_samples(model, cfg, exp_dir)
        
        print(f"  [OK] Semua hasil disimpan di: {exp_dir}")

    print(f"\n{'='*60}")
    print("  EVALUASI SELESAI")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()