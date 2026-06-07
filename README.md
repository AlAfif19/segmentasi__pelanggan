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
DB_HOST=localhost
DB_PORT=3306
DB_NAME=segmentasi_pelanggan
DB_USER=root
DB_PASSWORD=
```

Install dependency backend:

```bash
python -m pip install -r requirements.txt
```

Salin `.env.example` menjadi `.env`, lalu sesuaikan koneksi MySQL.

Inisialisasi schema dan load data dari `data_source/raw/`:

```bash
python data_source/loader/load_to_mysql.py
```

Data pelanggan dapat menggunakan `exported_data.csv` terbaru atau
`exported_data.xlsx` lama. Jika keduanya tersedia, loader memilih file yang
paling baru. Data transaksi tetap dibaca dari `exported_data_mutasi.xlsx`.

Halaman Proses Segmentasi mendukung periode 1 bulan, 3 bulan, 6 bulan, 1 tahun,
dan semua data sampai hari ini.

Jalankan backend pada terminal pertama:

```bash
python backend/app.py
```

Jalankan frontend pada terminal kedua:

```bash
npm install
npm run dev
```

Buka `http://localhost:5173`, kemudian login menggunakan akun seed:

```txt
Username: data_analyst
Password: password
```

Untuk build produksi frontend:

```bash
npm run build
```

## Catatan Loyalty

CSV pelanggan terbaru tidak memiliki kolom tanggal aktif. Dalam kondisi ini,
`active_date` disimpan sebagai `NULL` dan nilai Loyalty menjadi `0` untuk semua
pelanggan. Fitur konstan tersebut tidak memengaruhi jarak K-Means setelah scaling,
sehingga proses tetap aman secara komputasi, tetapi model secara efektif memakai
RFMC, bukan LRFMC penuh.

Gunakan XLSX yang memiliki `TGL AKTIF` bila penelitian harus mengevaluasi dimensi
Loyalty. Jangan mengganti tanggal aktif dengan `Masa Aktif`, `Jatuh Tempo`, atau
`Suspend` karena ketiganya memiliki makna berbeda.

## Benchmark Black-Box

Jalankan backend dan frontend, lalu:

```bash
npx playwright install chromium
npm run benchmark:blackbox
```

Untuk hasil yang dapat direplikasi, jalankan backend benchmark dengan
`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, dan `MKL_NUM_THREADS=1`.
Hasil agregat tersimpan di `docs/research/`.

Endpoint `POST /api/segmentation/run` akan membaca data MySQL, menghitung LRFMC, menjalankan K-Means Plus, menyimpan hasil cluster, lalu endpoint result/download akan mengambil data dari MySQL.
