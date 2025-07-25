# -*- coding: utf-8 -*-
"""Proyek Capstone HACKTIV8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TpvzdtgPK73taUIf8_1964TGbh5UV0AK
"""

# Cell 1: Import Library dan Konfigurasi Awal

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import numpy as np
import os

print(f"TensorFlow Version: {tf.__version__}")
print(f"Keras Version: {tf.keras.__version__}")

# --- Konfigurasi Dataset ---
# Path utama ke direktori 'mushroom_dataset' di Google Colab.
# Ini sudah dikonfirmasi sebagai '/content/dataset/mushroom_dataset'.
dataset_path = '/content/dataset/mushroom_dataset'

# --- Parameter Gambar ---
img_height = 128  # Tinggi gambar yang akan diubah ukurannya
img_width = 128   # Lebar gambar yang akan diubah ukurannya
batch_size = 32   # Jumlah gambar per batch untuk pelatihan

# --- Parameter Pembagian Data ---
validation_split = 0.2  # 20% data akan digunakan untuk validasi

print(f"\nDataset will be loaded from: {dataset_path}")
print(f"Target image dimensions: {img_height}x{img_width} pixels")
print(f"Batch size for training/validation: {batch_size}")
print(f"Validation data split: {validation_split*100}% of the dataset")

# Cell 2: Memverifikasi Path Dataset dan Struktur Direktori

print(f"Checking dataset path: {dataset_path}")

# Periksa apakah direktori dataset ada
if not os.path.exists(dataset_path):
    print(f"ERROR: Dataset path '{dataset_path}' not found!")
    print("Please ensure your 'mushroom_dataset' folder is correctly placed inside '/content/dataset'.")
    print("If you uploaded it, it should automatically be there. If using Google Drive, remember to mount it first:")
    print("  from google.colab import drive")
    print("  drive.mount('/content/drive')")
    print("And then adjust 'dataset_path' to point to your data on Drive (e.g., '/content/drive/MyDrive/path/to/mushroom_dataset').")

    # Opsional: Tampilkan isi dari /content/dataset jika ada
    content_dataset_root = '/content/dataset'
    if os.path.exists(content_dataset_root):
        print(f"\nContents of '{content_dataset_root}':")
        for item in os.listdir(content_dataset_root):
            print(f"- {item}")
    else:
        print(f"'{content_dataset_root}' also not found.")

else:
    print(f"Dataset found successfully at: {dataset_path}")
    print("\nListing subdirectories (classes) in 'mushroom_dataset':")
    try:
        class_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        if class_dirs:
            for class_name in sorted(class_dirs):
                class_path = os.path.join(dataset_path, class_name)
                num_images = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
                print(f"- {class_name}: Approximately {num_images} images")
        else:
            print("No class subdirectories found inside 'mushroom_dataset'. Make sure your images are organized into subfolders (e.g., 'deadly', 'edible').")
    except Exception as e:
        print(f"An error occurred while listing directories: {e}")

# Cell 3: Augmentasi dan Pemrosesan Data Menggunakan ImageDataGenerator

print("Configuring ImageDataGenerators...")

# Generator untuk data training (dengan augmentasi dan normalisasi)
train_datagen = ImageDataGenerator(
    rescale=1./255,          # Normalisasi nilai piksel dari [0, 255] ke [0, 1]
    shear_range=0.2,         # Shear transformation acak
    zoom_range=0.2,          # Zoom acak
    horizontal_flip=True,    # Membalik gambar secara horizontal acak
    validation_split=validation_split # Memisahkan sebagian data untuk validasi
)

# Generator untuk data validasi (hanya normalisasi, tanpa augmentasi)
validation_datagen = ImageDataGenerator(
    rescale=1./255,          # Normalisasi nilai piksel
    validation_split=validation_split # Memisahkan sebagian data untuk validasi
)

print("\nLoading training data from directory...")
train_generator = train_datagen.flow_from_directory(
    directory=dataset_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical', # Cocok untuk klasifikasi multi-kelas dengan one-hot encoding
    subset='training'         # Mengambil subset training
)

print("\nLoading validation data from directory...")
validation_generator = validation_datagen.flow_from_directory(
    directory=dataset_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'       # Mengambil subset validation
)

# Menampilkan informasi kelas yang terdeteksi
print("\nClasses detected by the generators (index: class_name):")
print(train_generator.class_indices)
num_classes = len(train_generator.class_indices)
print(f"Total number of classes: {num_classes}")

print(f"Found {train_generator.samples} training images belonging to {num_classes} classes.")
print(f"Found {validation_generator.samples} validation images belonging to {num_classes} classes.")

# Cell 4: Membangun dan Mengkompilasi Model CNN

print("Building the Convolutional Neural Network (CNN) model...")

model = Sequential([
    # Lapisan Konvolusi & MaxPooling Pertama
    # Input shape: (tinggi_gambar, lebar_gambar, jumlah_channel_warna)
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    # Lapisan Konvolusi & MaxPooling Kedua
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Lapisan Konvolusi & MaxPooling Ketiga
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Meratakan output dari lapisan konvolusi menjadi vektor 1D
    Flatten(),

    # Lapisan Fully Connected (Dense Layer)
    Dense(512, activation='relu'),
    Dropout(0.5), # Dropout layer untuk mengurangi overfitting (50% neuron dinonaktifkan secara acak)

    # Lapisan Output (Dense Layer)
    # Jumlah neuron sama dengan jumlah kelas, dengan aktivasi softmax untuk probabilitas
    Dense(num_classes, activation='softmax')
])

# Kompilasi Model
# Optimizer: 'adam' adalah pilihan yang baik untuk banyak tugas
# Loss function: 'categorical_crossentropy' karena kita menggunakan one-hot encoding untuk label
# Metrics: 'accuracy' untuk melacak akurasi selama pelatihan
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Menampilkan ringkasan arsitektur model
print("\nModel Summary:")
model.summary()

# Cell 5: Melatih Model

epochs = 20 # Anda bisa menyesuaikan jumlah epoch (iterasi penuh pada dataset pelatihan)

print(f"\nStarting model training for {epochs} epochs...")
print("This may take a while depending on your dataset size and Colab's allocated resources (GPU).")

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size, # Jumlah batch per epoch
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size # Jumlah batch validasi per epoch
)

print("\nModel training completed!")

# Cell 6: Evaluasi dan Visualisasi Hasil Training

# Evaluasi akhir model pada set validasi
print("\nEvaluating model performance on the validation set...")
loss, accuracy = model.evaluate(validation_generator)
print(f"Validation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy:.4f}")

# Visualisasi Grafik Akurasi dan Loss
plt.figure(figsize=(14, 6))

# Plot Akurasi
plt.subplot(1, 2, 1) # (rows, columns, panel_number)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.ylim([0, 1]) # Akurasi dari 0 hingga 1

# Plot Loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout() # Menyesuaikan tata letak untuk mencegah tumpang tindih
plt.show()