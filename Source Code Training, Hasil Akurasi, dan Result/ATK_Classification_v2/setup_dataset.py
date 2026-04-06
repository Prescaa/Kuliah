import splitfolders
import os

# 1. Tentukan folder sumber utama yang berisi sub-folder Pensil, Pulpen, dll.
# Di dalamnya, foto original (timestamp) dan augmented sudah bercampur
input_folder = 'Dataset_ATK_Preprocessed' 

# 2. Tentukan folder tujuan (akan dibuat otomatis oleh script ini)
output_folder = 'dataset'

# 3. Jalankan pembagian sesuai proporsi di config.py kamu (80% Train, 10% Val, 10% Test)
# Seed 1337 digunakan agar hasil pembagian acaknya tetap konsisten setiap kali dijalankan
splitfolders.ratio(input_folder, output=output_folder, seed=1337, ratio=(.8, .1, .1))

print("✅ Splitting selesai! Folder 'dataset' sekarang siap digunakan.")