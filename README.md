# Proyek Klasifikasi Jamur dengan Convolutional Neural Network (CNN)

## Pendahuluan

Proyek ini adalah bagian dari "Proyek Capstone HACKTIV8" yang berfokus pada pengembangan sistem klasifikasi gambar menggunakan _Deep Learning_. Tujuan utamanya adalah untuk mengidentifikasi dan mengkategorikan jenis jamur berdasarkan citra visualnya. Dengan meningkatnya minat pada jamur, baik untuk konsumsi, penelitian, atau tujuan lainnya, kemampuan untuk secara otomatis mengklasifikasikan spesies jamur menjadi sangat berharga.

## Tujuan Proyek

Tujuan utama dari proyek ini adalah:

1.  **Membangun Model Klasifikasi Gambar:** Mengembangkan sebuah model _Convolutional Neural Network_ (CNN) yang mampu mengidentifikasi berbagai jenis jamur dari gambar.
2.  **Meningkatkan Akurasi Identifikasi:** Melatih model agar dapat mencapai akurasi yang tinggi dalam membedakan antara spesies jamur yang berbeda, termasuk yang `conditionally_edible` (dapat dimakan bersyarat), `deadly` (mematikan), `edible` (dapat dimakan), dan `poisonous` (beracun).
3.  **Memanfaatkan Google Colab:** Mendemonstrasikan penggunaan Google Colab sebagai lingkungan pengembangan yang efisien, memanfaatkan sumber daya GPU-nya untuk mempercepat proses pelatihan model _deep learning_.
4.  **Memahami Proses End-to-End:** Memberikan pemahaman tentang seluruh alur kerja proyek _machine learning_ berbasis gambar, mulai dari persiapan data, pembangunan model, hingga evaluasi.

## Dataset

Dataset yang digunakan dalam proyek ini adalah kumpulan gambar jamur yang terorganisir dalam struktur direktori berdasarkan kategori atau jenis jamur. Struktur dataset di Google Colab diharapkan sebagai berikut:

```
/content/dataset/
└── mushroom_dataset/
    ├── conditionally_edible/  # Gambar jamur yang dapat dimakan bersyarat
    ├── deadly/                # Gambar jamur yang mematikan
    ├── edible/                # Gambar jamur yang dapat dimakan
    └── poisonous/             # Gambar jamur yang beracun

```

Setiap sub-direktori mewakili satu kelas jamur, dan berisi gambar-gambar yang termasuk dalam kelas tersebut.

## Teknologi dan Pendekatan

Proyek ini memanfaatkan beberapa teknologi dan pendekatan kunci dalam _machine learning_ dan _deep learning_:

-   **Python:** Bahasa pemrograman utama yang digunakan.
-   **TensorFlow & Keras:** _Framework_ _deep learning_ yang kuat untuk membangun, melatih, dan mengevaluasi model neural network. Keras menyediakan API tingkat tinggi yang mudah digunakan untuk prototipe cepat.
-   **Convolutional Neural Network (CNN):** Arsitektur neural network yang sangat efektif untuk tugas-tugas pengolahan citra. CNN secara otomatis dapat mempelajari fitur-fitur hierarkis dari gambar.
-   **Image Data Augmentation:** Teknik untuk meningkatkan variasi dataset pelatihan dengan menerapkan transformasi acak pada gambar (misalnya, rotasi, zoom, flipping). Ini membantu model menjadi lebih kuat dan mengurangi _overfitting_.
-   **Google Colab:** Platform _cloud-based_ gratis yang menyediakan akses ke GPU, sangat ideal untuk menjalankan eksperimen _deep learning_ tanpa memerlukan perangkat keras lokal yang kuat.

## Cara Kerja Program (Ringkasan)

Program ini diimplementasikan dalam beberapa tahapan utama di Google Colab:

1.  **Inisialisasi & Konfigurasi:** Mengimpor library yang dibutuhkan dan mengatur parameter global seperti ukuran gambar target (`128x128` piksel), ukuran _batch_, dan rasio pembagian data untuk pelatihan dan validasi.
2.  **Validasi Dataset:** Memverifikasi keberadaan dan struktur dataset di lokasi yang ditentukan (`/content/dataset/mushroom_dataset`). Ini memastikan bahwa program dapat mengakses gambar dengan benar.
3.  **Persiapan Data dengan `ImageDataGenerator`:**
    -   Menggunakan `tf.keras.preprocessing.image.ImageDataGenerator` untuk secara efisien memuat gambar dari direktori.
    -   Melakukan normalisasi piksel (menskalakan nilai piksel dari 0-255 ke 0-1).
    -   Menerapkan augmentasi data pada set pelatihan untuk meningkatkan robustnes model.
    -   Membagi dataset menjadi set pelatihan (80%) dan validasi (20%).
4.  **Pembangunan & Kompilasi Model CNN:**
    -   Membangun arsitektur CNN sekuensial yang terdiri dari beberapa lapisan konvolusi (`Conv2D`) diikuti oleh lapisan _max-pooling_ (`MaxPooling2D`) untuk ekstraksi fitur.
    -   Lapisan `Flatten` digunakan untuk mengubah output konvolusional menjadi vektor 1D.
    -   Model diakhiri dengan lapisan _dense_ (`Dense`) dan lapisan _dropout_ (`Dropout`) untuk klasifikasi dan pencegahan _overfitting_.
    -   Model dikompilasi dengan _optimizer_ `Adam` dan _loss function_ `categorical_crossentropy` (sesuai untuk klasifikasi multi-kelas).
5.  **Pelatihan Model:**
    -   Model dilatih menggunakan metode `model.fit()` dengan data dari generator pelatihan dan divalidasi dengan data dari generator validasi selama sejumlah _epoch_ tertentu.
6.  **Evaluasi & Visualisasi Hasil:**
    -   Setelah pelatihan, model dievaluasi pada set validasi untuk mendapatkan metrik _loss_ dan _accuracy_ akhir.
    -   Grafik visual dari akurasi pelatihan/validasi dan _loss_ pelatihan/validasi digeneralisasi untuk memantau performa model sepanjang _epoch_.

## Hasil

Output utama dari menjalankan program ini adalah:

-   Statistik mengenai jumlah gambar yang dimuat dan jumlah kelas yang terdeteksi.
-   Ringkasan arsitektur model CNN yang dibuat.
-   Catatan progres pelatihan model, menampilkan _loss_ dan _accuracy_ untuk set pelatihan dan validasi di setiap _epoch_.
-   Hasil evaluasi akhir model yang menunjukkan akurasi dan _loss_ pada set validasi.
-   Dua plot grafik yang menunjukkan tren akurasi dan _loss_ selama pelatihan, yang sangat berguna untuk mengidentifikasi _overfitting_ atau _underfitting_.

Proyek ini memberikan dasar yang kuat untuk klasifikasi gambar jamur, dan dapat dikembangkan lebih lanjut dengan arsitektur model yang lebih kompleks, transfer learning, atau teknik optimasi lainnya.

----------
