# Sistem Segmentasi Pelanggan

Sistem ini digunakan untuk melakukan segmentasi pelanggan berdasarkan nilai transaksi perusahaan menggunakan algoritma K-Means Plus dan framework CRISP-DM.

## Teknologi

- Frontend: React, Vite, Tailwind CSS, Framer Motion
- Backend: Python Flask
- Machine Learning: scikit-learn
- Database: MySQL
- Export: CSV, Excel, JSON

## Fitur

1. Login Data Analyst
2. Data Tertanam
3. Proses Segmentasi
4. Lihat Hasil dengan filter pencarian pelanggan
5. Identifikasi status pembayaran tepat waktu/sering terlambat
6. Download Result

## Catatan

Sistem tidak menggunakan Upload CSV.  
Sistem tidak menggunakan Create Project.  
Sistem tidak menggunakan K-Means klasik.  
Data pelanggan dan transaksi sudah tertanam di database MySQL.

## Integrasi MySQL

Pastikan MySQL berjalan dan sesuaikan `.env`:

```txt
APP_DEBUG=False
SECRET_KEY=replace_with_a_strong_secret_key
DB_HOST=localhost
DB_PORT=3306
DB_NAME=segmentasi_pelanggan
DB_USER=segmentasi_user
DB_PASSWORD=replace_with_database_password
ANALYST_USERNAME=data_analyst
ANALYST_PASSWORD=replace_with_initial_password
```

Install dependency backend:

```bash
python -m pip install -r requirements.txt
```

Inisialisasi schema dan load data Excel dari `data_source/raw/`:

```bash
python data_source/loader/load_to_mysql.py
```

Jalankan backend:

```bash
python backend/app.py
```

Endpoint `POST /api/segmentation/run` akan membaca data MySQL, menghitung LRFMC, menjalankan K-Means Plus, menyimpan hasil cluster, lalu endpoint result/download akan mengambil data dari MySQL.
