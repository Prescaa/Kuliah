import os
import joblib
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage.io import imread
from skimage.transform import resize
from config import RESULTS_DIR, CLASS_NAMES

def extract_features(image_path, size):
    img = imread(image_path, as_gray=True)
    img_res = resize(img, size)
    fd = hog(img_res, orientations=11, pixels_per_cell=(8, 8), 
             cells_per_block=(2, 2), visualize=False)
    return fd, img_res

def predict_image(image_path):
    # Menggunakan model dari Eksperimen 3 (Hasil Terbaik)
    model_path = os.path.join(RESULTS_DIR, "eksperimen_3", "model_ml1.pkl")
    
    if not os.path.exists(model_path):
        print("[ERROR] Model eksperimen_3 tidak ditemukan. Jalankan train.py dulu.")
        return

    model = joblib.load(model_path)
    features, img_display = extract_features(image_path, (128, 128))
    
    prediction = model.predict([features])[0]
    prob = model.predict_proba([features])[0]
    
    label = CLASS_NAMES[prediction]
    conf = prob[prediction] * 100

    plt.imshow(img_display, cmap='gray')
    plt.title(f"Prediksi: {label} ({conf:.2f}%)")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Ganti nama file di bawah ini dengan foto yang ingin Anda tes
    test_file = "tes_atk.jpg"
    if os.path.exists(test_file):
        predict_image(test_file)
    else:
        print(f"File {test_file} tidak ditemukan di folder proyek.")