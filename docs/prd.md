# PRODUCT REQUIREMENT DOCUMENT  
# Sistem Segmentasi Pelanggan Berbasis Web Menggunakan K-Means Plus dan CRISP-DM

## 1. Identitas Produk

Nama produk: Sistem Segmentasi Pelanggan  
Aktor utama: Data Analyst  
Platform: Web  
Database: MySQL  
Metode utama: K-Means Plus  
Framework analisis: CRISP-DM  
Data input: Data pelanggan dan data transaksi yang sudah tertanam di sistem  
Fitur utama: Login, Proses Segmentasi, Lihat Hasil, Search Data, Download Result  

Sistem ini dirancang berdasarkan kebutuhan penelitian segmentasi pelanggan PT Nuansa Teknologi Informasi. Sistem memproses data pelanggan dan data mutasi transaksi melalui tahapan CRISP-DM, lalu menghasilkan cluster pelanggan berbasis nilai transaksi menggunakan K-Means Plus. Rancangan ini mengikuti laporan penelitian yang membahas segmentasi pelanggan, LRFMC, K-Means Plus, evaluasi model, dan implementasi berbasis web. :contentReference[oaicite:0]{index=0}

---

## 2. Ringkasan Produk

Sistem Segmentasi Pelanggan adalah aplikasi web yang digunakan oleh Data Analyst untuk menjalankan proses segmentasi pelanggan secara otomatis.

Data Analyst tidak perlu mengunggah file CSV. Data sudah tertanam di dalam sistem dan tersimpan di database MySQL.

Data Analyst hanya perlu login, membuka halaman proses segmentasi, lalu menekan tombol start pipeline. Setelah itu sistem menjalankan proses CRISP-DM secara berurutan.

Tahapan sistem terdiri dari:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

Pada tahap modeling, sistem hanya menggunakan algoritma K-Means Plus. Sistem tidak menggunakan K-Means klasik.

Hasil akhir ditampilkan dalam halaman Lihat Hasil. Data Analyst dapat melihat karakteristik cluster, tabel hasil pelanggan, mencari data pelanggan, dan mengunduh hasil segmentasi.

---

## 3. Tujuan Produk

Tujuan utama sistem adalah membantu Data Analyst melakukan segmentasi pelanggan secara terstruktur, otomatis, dan mudah diakses melalui browser.

Tujuan sistem:

1. Mengotomatisasi proses segmentasi pelanggan berbasis CRISP-DM.
2. Menggunakan data pelanggan dan transaksi yang sudah tertanam di sistem.
3. Mengolah data menjadi fitur LRFMC.
4. Menjalankan algoritma K-Means Plus.
5. Menghasilkan cluster pelanggan.
6. Memberikan label segmen seperti Low-Value, Medium-Value, dan High-Value.
7. Menampilkan hasil evaluasi model.
8. Menyediakan pencarian data pelanggan.
9. Menyediakan unduhan hasil segmentasi.
10. Menyimpan data dan hasil proses ke MySQL.

---

## 4. Batasan Sistem

Sistem ini memiliki batasan berikut:

1. Sistem hanya memiliki satu aktor, yaitu Data Analyst.
2. Sistem tidak memiliki fitur Upload CSV.
3. Sistem tidak memiliki fitur Create Project.
4. Sistem tidak menggunakan K-Means klasik.
5. Sistem hanya menggunakan algoritma K-Means Plus.
6. Sistem menggunakan database MySQL.
7. Data pelanggan dan transaksi sudah tertanam di sistem.
8. Sistem hanya berjalan melalui web browser.
9. Sistem tidak dikembangkan sebagai aplikasi mobile.
10. Sistem tidak memiliki role admin.
11. Sistem tidak memiliki fitur edit data manual.
12. Sistem tidak memakai algoritma clustering lain.
13. Sistem hanya berfokus pada segmentasi pelanggan berdasarkan nilai transaksi.
14. Sistem memakai evaluasi Elbow Method, Silhouette Score, Davies-Bouldin Index, dan Calinski-Harabasz Index.

---

## 5. Aktor Sistem

## 5.1 Data Analyst

Data Analyst adalah pengguna utama sistem.

Hak akses Data Analyst:

1. Login ke sistem.
2. Membuka dashboard.
3. Menjalankan proses segmentasi.
4. Melihat hasil segmentasi.
5. Melihat evaluasi model.
6. Mencari data pelanggan.
7. Mengunduh hasil segmentasi.
8. Logout dari sistem.

---

## 6. Fitur Utama Sistem

Fitur utama sistem terdiri dari:

1. Login
2. Proses Segmentasi
3. Lihat Hasil
4. Search Data
5. Download Result

Relasi fitur:

1. Data Analyst harus login sebelum menjalankan fitur lain.
2. Proses Segmentasi membutuhkan login.
3. Lihat Hasil dapat diakses setelah proses segmentasi selesai.
4. Search Data menjadi perluasan dari Lihat Hasil.
5. Download Result menjadi perluasan dari Lihat Hasil.

---

## 7. Use Case Sistem

## 7.1 Use Case Login

Nama use case: Login  
Aktor: Data Analyst  
Tujuan: Masuk ke sistem segmentasi pelanggan  

Alur utama:

1. Data Analyst membuka halaman login.
2. Sistem menampilkan form login.
3. Data Analyst memasukkan username dan password.
4. Sistem memvalidasi akun ke database MySQL.
5. Sistem memberi akses jika data valid.
6. Sistem menampilkan halaman utama.

Alur alternatif:

1. Data Analyst memasukkan username atau password yang salah.
2. Sistem menampilkan pesan bahwa username atau password salah.
3. Data Analyst mengisi ulang form login.

Kondisi akhir:

Data Analyst berhasil masuk ke sistem.

---

## 7.2 Use Case Proses Segmentasi

Nama use case: Proses Segmentasi  
Aktor: Data Analyst  
Tujuan: Menjalankan pipeline segmentasi pelanggan  

Alur utama:

1. Data Analyst membuka halaman Proses Segmentasi.
2. Sistem menampilkan progress log.
3. Data Analyst menekan tombol start pipeline.
4. Sistem mengambil data dari database.
5. Sistem membersihkan missing value dan outlier.
6. Sistem menghapus data duplikat.
7. Sistem melakukan transformasi data.
8. Sistem menghitung LRFMC.
9. Sistem melakukan normalisasi data.
10. Sistem menjalankan K-Means Plus.
11. Sistem menghitung evaluasi model.
12. Sistem menyimpan hasil clustering, labeling, dan skor evaluasi.
13. Sistem menampilkan status cluster selesai.

Alur alternatif:

1. Data tertanam belum tersedia.
2. Sistem menampilkan pesan bahwa data tidak tersedia.
3. Sistem menghentikan proses.

Kondisi akhir:

Hasil segmentasi tersimpan di database.

---

## 7.3 Use Case Lihat Hasil

Nama use case: Lihat Hasil  
Aktor: Data Analyst  
Tujuan: Melihat hasil cluster pelanggan  

Alur utama:

1. Data Analyst membuka halaman Lihat Hasil.
2. Sistem mengambil hasil clustering dari database.
3. Sistem menampilkan grafik jumlah pelanggan per segmen.
4. Sistem menampilkan karakteristik cluster.
5. Sistem menampilkan tabel hasil pelanggan.
6. Sistem menampilkan tombol Search Data.
7. Sistem menampilkan tombol Download Result.

Alur alternatif:

1. Hasil segmentasi belum tersedia.
2. Sistem menampilkan pesan bahwa proses segmentasi harus dijalankan terlebih dahulu.

Kondisi akhir:

Data Analyst dapat melihat hasil segmentasi.

---

## 7.4 Use Case Search Data

Nama use case: Search Data  
Aktor: Data Analyst  
Tujuan: Mencari data pelanggan hasil segmentasi  

Alur utama:

1. Data Analyst membuka halaman Search Data.
2. Data Analyst memilih kategori pencarian.
3. Data Analyst memasukkan kata kunci.
4. Data Analyst memilih filter segmen.
5. Sistem mencari data pada hasil segmentasi.
6. Sistem menampilkan daftar hasil pencarian.
7. Data Analyst memilih salah satu pelanggan.
8. Sistem menampilkan detail pelanggan.

Alur alternatif:

1. Data tidak ditemukan.
2. Sistem menampilkan pesan data tidak ditemukan.

Kondisi akhir:

Data pelanggan yang dicari tampil dengan detail segmen.

---

## 7.5 Use Case Download Result

Nama use case: Download Result  
Aktor: Data Analyst  
Tujuan: Mengunduh hasil segmentasi  

Alur utama:

1. Data Analyst membuka halaman Download Result.
2. Sistem menampilkan pilihan format export.
3. Data Analyst memilih format CSV, Excel, atau JSON.
4. Data Analyst memilih komponen yang ingin disertakan.
5. Sistem mengambil data hasil segmentasi.
6. Sistem membuat file hasil.
7. Sistem mengunduh file ke perangkat pengguna.

Alur alternatif:

1. Tidak ada data hasil segmentasi.
2. Sistem menampilkan pesan tidak ada data untuk diunduh.

Kondisi akhir:

File hasil segmentasi berhasil diunduh.

---

## 8. Alur Activity Diagram Proses Segmentasi

Activity Diagram Proses Segmentasi memiliki dua swimlane:

1. Data Analyst
2. Sistem

Alur proses:

1. Data Analyst memulai proses segmentasi.
2. Sistem melakukan cleaning, duplicate handling, transformasi data, dan normalisasi.
3. Sistem menghasilkan data clean.
4. Sistem menghitung jarak D(x)² ke centroid terdekat.
5. Sistem menghitung probabilitas P(x) sebanding dengan D(x)².
6. Sistem memilih centroid berikutnya.
7. Sistem memeriksa apakah jumlah centroid sudah mencapai K.
8. Jika belum, sistem mengulang perhitungan jarak dan probabilitas.
9. Jika sudah, sistem melakukan assign data ke centroid.
10. Sistem melakukan update centroid berdasarkan mean cluster.
11. Sistem memeriksa apakah centroid berubah atau iterasi sudah mencapai batas maksimum.
12. Jika centroid masih berubah, sistem mengulang proses assignment.
13. Jika centroid tidak berubah, sistem menghitung metrik evaluasi.
14. Sistem menghitung Silhouette Score.
15. Sistem menghitung Davies-Bouldin Index.
16. Sistem menghitung Calinski-Harabasz Index.
17. Sistem menyimpan hasil clustering, labeling, dan evaluation.
18. Sistem menampilkan status cluster selesai.

---

## 9. Alur Sequence Diagram Proses Segmentasi

Objek utama:

1. Data Analyst
2. Proses Segmentasi
3. Database

Alur sequence:

1. Data Analyst menjalankan startPipeline().
2. Proses Segmentasi meminta data dengan getRows().
3. Database mengirim data pelanggan dan transaksi.
4. Sistem melakukan clean missing value dan outlier.
5. Sistem menghapus duplikat.
6. Sistem menghitung calculateLoyalty().
7. Sistem menghitung calculateRecency().
8. Sistem menghitung calculateFrequency().
9. Sistem menghitung calculateMonetary().
10. Sistem menghitung calculateCategory().
11. Sistem menjalankan normalizeData().
12. Sistem menjalankan initializeCentroids().
13. Sistem menjalankan loop sampai konvergen.
14. Sistem menjalankan assignClusters().
15. Sistem menjalankan updateCentroids().
16. Sistem menjalankan convergenceCheck().
17. Sistem menghitung calculateElbow().
18. Sistem menghitung calculateDBI().
19. Sistem menghitung calculateCHI().
20. Sistem menghitung calculateSilhouette().
21. Sistem menyimpan clustering, labeling LRFMC, dan evaluation score.
22. Database menyimpan hasil melalui post_result().
23. Database mengembalikan getid_result().
24. Data Analyst menerima status hasil segmentasi.

---

## 10. Class Diagram Sistem

## 10.1 Class Data Analyst

Atribut:

1. id_dataAnalyst: int
2. username: string
3. password: string
4. role: string
5. created_at: date

Method:

1. login(): int
2. logout(): int
3. searchResult(): int
4. downloadResult(): int
5. getid_result(): int

Catatan:

Method createProject() harus dihapus karena sistem tidak memakai fitur Create Project.

---

## 10.2 Class Login

Atribut:

1. id_login: int
2. timestamp: date

Method:

1. getid_dataAnalyst(): int

Fungsi:

Class Login menyimpan proses autentikasi pengguna.

---

## 10.3 Class Dataset

Atribut:

1. id_dataset: int
2. filename: string
3. row_count: int
4. loaded_at: date

Method:

1. validateData(): int
2. previewData(): int
3. getRows(): int

Catatan:

Nama atribut upload_date perlu diganti menjadi loaded_at karena sistem tidak memiliki upload CSV.

---

## 10.4 Class LRFMC_Transformation

Atribut:

1. id_lrfmc: int
2. customer_id: string
3. loyalty: float
4. recency: float
5. frequency: int
6. monetary: float
7. category: string

Method:

1. calculateLoyalty(): int
2. calculateRecency(): int
3. calculateFrequency(): int
4. calculateMonetary(): int
5. calculateCategory(): int
6. normalizeData(): int

Fungsi:

Class ini mengubah data pelanggan dan transaksi menjadi fitur LRFMC.

---

## 10.5 Class Model

Atribut:

1. id_model: int
2. k_value: int
3. algorithm_name: string
4. iteration: int

Method:

1. initializeCentroids(): int
2. assignClusters(): int
3. updateCentroids(): int
4. convergeCheck(): int

Fungsi:

Class Model menjalankan algoritma K-Means Plus.

Catatan:

Nilai algorithm_name harus bernilai K-Means Plus.

---

## 10.6 Class EvaluationMetrics

Atribut:

1. id_eval: int
2. elbowmethod: int
3. davies_bouldin: float
4. calinski_harabasz: float
5. silhouette_avg: float

Method:

1. calculateElbow(): int
2. calculateDBI(): int
3. calculateCHI(): int
4. calculateSilhouette(): int

Fungsi:

Class ini menghitung kualitas hasil cluster.

---

## 10.7 Class ClusterResult

Atribut:

1. id_result: int
2. segment_label: string
3. file_result: string

Method:

1. getid_model(): int
2. getid_eval(): int
3. getid_dataset(): int

Fungsi:

Class ini menyimpan hasil segmentasi pelanggan.

---

## 11. Component Diagram Sistem

Komponen utama:

1. Frontend
2. Controller
3. API Gateway
4. Auth Service
5. Segmentation Service
6. Data Preprocessing Service
7. Clustering Service
8. Evaluation Service
9. File Storage Service
10. Database Service
11. MySQL Database

## 11.1 Frontend

File utama:

main.py atau halaman frontend sesuai implementasi.

Fungsi:

1. Menampilkan halaman login.
2. Menampilkan progress proses segmentasi.
3. Menampilkan hasil segmentasi.
4. Menampilkan halaman search.
5. Menampilkan halaman download.

## 11.2 API Gateway

File utama:

routes.py

Fungsi:

1. Menerima request dari frontend.
2. Mengarahkan request ke service yang sesuai.
3. Mengatur routing proses login, segmentasi, hasil, search, dan download.

## 11.3 Auth Service

File utama:

auth.py

Fungsi:

1. Memvalidasi username dan password.
2. Membuat sesi pengguna.
3. Mengatur logout.

## 11.4 Segmentation Service

File utama:

segmentation.py

Fungsi:

1. Menjalankan pipeline segmentasi.
2. Mengatur alur CRISP-DM.
3. Memanggil preprocessing, clustering, dan evaluation service.

## 11.5 Data Preprocessing Service

File utama:

preprocessing.py

Fungsi:

1. Membersihkan missing value.
2. Menghapus duplikasi.
3. Mengubah data menjadi fitur LRFMC.
4. Melakukan normalisasi data.

## 11.6 Clustering Service

File utama:

clustering.py

Fungsi:

1. Menjalankan K-Means Plus.
2. Menginisialisasi centroid.
3. Melakukan assignment data.
4. Melakukan update centroid.
5. Mengecek konvergensi.

## 11.7 Evaluation Service

File utama:

evaluation.py

Fungsi:

1. Menghitung Elbow Method.
2. Menghitung Silhouette Score.
3. Menghitung Davies-Bouldin Index.
4. Menghitung Calinski-Harabasz Index.

## 11.8 File Storage Service

File utama:

storage.py

Fungsi:

1. Menyimpan file hasil export.
2. Menyiapkan file download CSV.
3. Menyiapkan file download Excel.
4. Menyiapkan file download JSON.

## 11.9 Database Service

File utama:

cluster.sql

Fungsi:

1. Menyimpan data pelanggan.
2. Menyimpan data transaksi.
3. Menyimpan hasil LRFMC.
4. Menyimpan hasil cluster.
5. Menyimpan skor evaluasi.

---

## 12. Deployment Diagram Sistem

Node deployment:

1. Client Device
2. Web Server
3. Application Server
4. Database Server
5. File Storage Server
6. Data Source Server

## 12.1 Client Device

Komponen:

1. Web Browser

Fungsi:

Data Analyst mengakses sistem melalui browser.

## 12.2 Web Server

Komponen:

1. Frontend

Fungsi:

Menyediakan tampilan web untuk pengguna.

## 12.3 Application Server

Komponen:

1. API Gateway
2. Auth Service
3. Segmentation Service

Fungsi:

Menjalankan logika aplikasi, autentikasi, dan pipeline segmentasi.

## 12.4 Database Server

Komponen:

1. MySQL

Fungsi:

Menyimpan seluruh data dan hasil proses.

## 12.5 File Storage Server

Komponen:

1. File Storage

Fungsi:

Menyimpan file hasil export.

## 12.6 Data Source Server

Komponen:

1. Source Data

Fungsi:

Menjadi sumber awal data pelanggan dan transaksi yang dimasukkan ke sistem.

Catatan:

Data Source Server hanya dipakai untuk load atau import data awal. Data Analyst tidak melakukan upload CSV dari antarmuka sistem.

---

## 13. Interface Sistem

## 13.1 Halaman Login

Komponen:

1. Judul Sistem Segmentasi Pelanggan.
2. Label Login Data Analyst.
3. Pesan error jika login gagal.
4. Input Data Analyst name.
5. Input password.
6. Tombol Login.
7. Link lupa password.

Fungsi:

Halaman ini memastikan hanya Data Analyst yang valid dapat masuk ke sistem.

Validasi:

1. Username wajib diisi.
2. Password wajib diisi.
3. Sistem menampilkan pesan jika username atau password salah.

---

## 13.2 Halaman Proses Segmentasi

Komponen utama:

1. Progress Log.
2. Evaluasi Model.
3. Tombol Lihat Hasil.

Progress log menampilkan:

1. Cleaning missing values.
2. Removing duplicate data.
3. Transforming numeric data.
4. Calculating LRFMC.
5. Normalizing data.
6. Configuring K=3 and max_iter=300.
7. Initializing first centroid.
8. Calculating D(x)².
9. Calculating P(x).
10. Selecting new centroid.
11. Assigning data to centroid.
12. Updating centroid.
13. Checking convergence.

Evaluasi model menampilkan:

1. DBI.
2. CHI.
3. Silhouette Score.
4. Cluster Count.

Fungsi:

Halaman ini menampilkan proses segmentasi secara transparan.

---

## 13.3 Halaman Lihat Hasil

Komponen:

1. Bar chart jumlah pelanggan per segmen.
2. Tabel karakteristik cluster.
3. Tabel hasil pelanggan.
4. Tombol Search Data.
5. Tombol Download Result.

Tabel karakteristik cluster berisi:

1. Cluster.
2. Label segmen.
3. Avg Recency.
4. Avg Frequency.
5. Avg Monetary.
6. Jumlah pelanggan.
7. Interpretasi.

Tabel hasil pelanggan berisi:

1. Customer ID.
2. Nama.
3. R.
4. F.
5. M.
6. Cluster.
7. Segment Label.

Fungsi:

Halaman ini menjadi pusat analisis hasil segmentasi.

---

## 13.4 Halaman Search Data

Komponen:

1. Dropdown cari berdasarkan.
2. Input kata kunci.
3. Dropdown filter segmen.
4. Tombol Cari.
5. Tabel hasil pencarian.
6. Panel detail pelanggan.

Tabel hasil pencarian berisi:

1. Pilih.
2. Customer ID.
3. Nama pelanggan.
4. Segmen.
5. Cluster.
6. R.
7. F.
8. M.
9. Rekomendasi.

Panel detail pelanggan berisi:

1. Baris yang dipilih.
2. Profil pelanggan.
3. Nilai RFM.
4. Label segmen.
5. Cluster.
6. Status hasil.

Fungsi:

Halaman ini membantu Data Analyst menemukan pelanggan tertentu tanpa membaca semua tabel hasil.

---

## 13.5 Halaman Download Result

Komponen:

1. Pilihan format CSV.
2. Pilihan format Excel.
3. Pilihan format JSON.
4. Opsi sertakan metadata.
5. Opsi sertakan skor evaluasi.
6. Opsi sertakan detail RFM.
7. Opsi sertakan label segmen.
8. Pesan status data.
9. Tombol Download.
10. Tombol Cancel.

Fungsi:

Halaman ini digunakan untuk mengunduh hasil segmentasi.

Catatan:

Tulisan metadata project perlu diganti menjadi metadata proses karena sistem tidak memakai Create Project.

---

## 14. Data dan Fitur LRFMC

Fitur LRFMC digunakan sebagai dasar segmentasi pelanggan.

## 14.1 Loyalty

Definisi:

Loyalty menunjukkan lama hubungan pelanggan dengan perusahaan.

Rumus:

Tanggal analisis dikurangi tanggal aktif pelanggan.

Sumber data:

TGL AKTIF pada data pelanggan.

## 14.2 Recency

Definisi:

Recency menunjukkan seberapa baru pelanggan melakukan transaksi.

Rumus:

Tanggal analisis dikurangi tanggal transaksi terakhir.

Sumber data:

TANGGAL pada data mutasi transaksi.

## 14.3 Frequency

Definisi:

Frequency menunjukkan jumlah transaksi pelanggan.

Rumus:

Jumlah transaksi pelanggan dengan UANG MASUK lebih dari 0.

Sumber data:

Data mutasi transaksi.

## 14.4 Monetary

Definisi:

Monetary menunjukkan total nilai uang masuk dari pelanggan.

Rumus:

Total UANG MASUK per pelanggan.

Sumber data:

UANG MASUK pada data mutasi transaksi.

## 14.5 Category

Definisi:

Category menunjukkan kategori layanan pelanggan.

Rumus:

Paket layanan dikonversi menjadi nilai ordinal.

Sumber data:

PAKET pada data pelanggan.

---

## 15. Proses K-Means Plus

Tahapan K-Means Plus:

1. Sistem memilih centroid pertama.
2. Sistem menghitung jarak setiap data ke centroid terdekat.
3. Sistem menghitung D(x)².
4. Sistem menghitung probabilitas P(x) yang sebanding dengan D(x)².
5. Sistem memilih centroid berikutnya.
6. Sistem mengulang proses sampai jumlah centroid sama dengan K.
7. Sistem melakukan assignment data ke centroid terdekat.
8. Sistem melakukan update centroid menggunakan rata-rata anggota cluster.
9. Sistem mengecek perubahan centroid.
10. Sistem berhenti jika centroid tidak berubah atau iterasi mencapai batas maksimum.

Parameter awal:

1. K = 3.
2. max_iter = 300.
3. Algoritma = K-Means Plus.
4. Data input = fitur LRFMC yang sudah dinormalisasi.

---

## 16. Evaluasi Model

Evaluasi model digunakan untuk mengukur kualitas cluster.

## 16.1 Elbow Method

Fungsi:

Menentukan kandidat jumlah cluster terbaik berdasarkan nilai SSE.

Interpretasi:

Nilai SSE yang lebih rendah menunjukkan data lebih dekat ke centroid. Titik elbow dipakai sebagai dasar pemilihan jumlah cluster yang seimbang.

## 16.2 Silhouette Score

Fungsi:

Mengukur kedekatan data dengan cluster sendiri dibanding cluster lain.

Interpretasi:

Nilai lebih tinggi menunjukkan kualitas cluster lebih baik.

## 16.3 Davies-Bouldin Index

Fungsi:

Mengukur rasio antara sebaran internal cluster dan jarak antar centroid.

Interpretasi:

Nilai lebih rendah menunjukkan cluster lebih baik.

## 16.4 Calinski-Harabasz Index

Fungsi:

Mengukur perbandingan variasi antar cluster dan variasi dalam cluster.

Interpretasi:

Nilai lebih tinggi menunjukkan cluster lebih baik.

---

## 17. Segment Label

Sistem menghasilkan tiga label utama.

## 17.1 Low-Value

Karakteristik:

1. Monetary rendah.
2. Frequency rendah.
3. Recency tinggi.
4. Aktivitas transaksi rendah.

Rekomendasi:

Kampanye reaktivasi pelanggan.

## 17.2 Medium-Value

Karakteristik:

1. Monetary sedang.
2. Frequency cukup stabil.
3. Recency sedang.
4. Potensi peningkatan layanan.

Rekomendasi:

Penawaran paket menengah dan program retensi.

## 17.3 High-Value

Karakteristik:

1. Monetary tinggi.
2. Frequency tinggi.
3. Recency rendah.
4. Pelanggan aktif dan bernilai tinggi.

Rekomendasi:

Prioritas loyalty reward dan upselling layanan premium.

---

## 18. Database MySQL

## 18.1 Tabel data_analyst

Fungsi:

Menyimpan akun pengguna sistem.

Kolom:

1. id_dataAnalyst INT PRIMARY KEY AUTO_INCREMENT
2. username VARCHAR(100)
3. password VARCHAR(255)
4. role VARCHAR(50)
5. created_at DATETIME

---

## 18.2 Tabel login

Fungsi:

Menyimpan riwayat login.

Kolom:

1. id_login INT PRIMARY KEY AUTO_INCREMENT
2. id_dataAnalyst INT
3. timestamp DATETIME
4. status VARCHAR(50)

---

## 18.3 Tabel dataset

Fungsi:

Menyimpan metadata data tertanam.

Kolom:

1. id_dataset INT PRIMARY KEY AUTO_INCREMENT
2. filename VARCHAR(255)
3. row_count INT
4. loaded_at DATETIME

Catatan:

Kolom loaded_at digunakan karena data berasal dari sistem, bukan dari upload pengguna.

---

## 18.4 Tabel customers

Fungsi:

Menyimpan data master pelanggan.

Kolom:

1. id_customer INT PRIMARY KEY AUTO_INCREMENT
2. nopel VARCHAR(50)
3. nama_pelanggan VARCHAR(150)
4. paket VARCHAR(100)
5. tarif_bulan DECIMAL(15,2)
6. total_tarif DECIMAL(15,2)
7. status VARCHAR(50)
8. tgl_aktif DATE
9. berakhir DATE
10. tgl_jatuh_tempo DATE
11. isolir VARCHAR(20)

---

## 18.5 Tabel transactions

Fungsi:

Menyimpan data transaksi pelanggan.

Kolom:

1. id_transaction INT PRIMARY KEY AUTO_INCREMENT
2. nopel VARCHAR(50)
3. tanggal DATETIME
4. transaksi VARCHAR(100)
5. pembayaran VARCHAR(100)
6. keterangan TEXT
7. uang_masuk DECIMAL(15,2)
8. uang_keluar DECIMAL(15,2)
9. data_analyst VARCHAR(100)

---

## 18.6 Tabel lrfmc_transformation

Fungsi:

Menyimpan hasil transformasi LRFMC.

Kolom:

1. id_lrfmc INT PRIMARY KEY AUTO_INCREMENT
2. id_dataset INT
3. customer_id VARCHAR(50)
4. loyalty FLOAT
5. recency FLOAT
6. frequency INT
7. monetary FLOAT
8. category VARCHAR(100)
9. loyalty_scaled FLOAT
10. recency_scaled FLOAT
11. frequency_scaled FLOAT
12. monetary_scaled FLOAT
13. category_scaled FLOAT

---

## 18.7 Tabel model

Fungsi:

Menyimpan data model K-Means Plus.

Kolom:

1. id_model INT PRIMARY KEY AUTO_INCREMENT
2. k_value INT
3. algorithm_name VARCHAR(100)
4. iteration INT
5. created_at DATETIME

---

## 18.8 Tabel evaluation_metrics

Fungsi:

Menyimpan skor evaluasi model.

Kolom:

1. id_eval INT PRIMARY KEY AUTO_INCREMENT
2. id_model INT
3. elbowmethod FLOAT
4. davies_bouldin FLOAT
5. calinski_harabasz FLOAT
6. silhouette_avg FLOAT

---

## 18.9 Tabel cluster_result

Fungsi:

Menyimpan hasil segmentasi.

Kolom:

1. id_result INT PRIMARY KEY AUTO_INCREMENT
2. id_model INT
3. id_eval INT
4. id_dataset INT
5. customer_id VARCHAR(50)
6. cluster INT
7. segment_label VARCHAR(100)
8. file_result VARCHAR(255)

---

## 19. Endpoint API

## 19.1 Auth API

POST /api/login

Fungsi:

Memproses login Data Analyst.

POST /api/logout

Fungsi:

Memproses logout Data Analyst.

---

## 19.2 Segmentation API

POST /api/segmentation/start

Fungsi:

Menjalankan pipeline segmentasi.

GET /api/segmentation/progress

Fungsi:

Mengambil progress log segmentasi.

GET /api/segmentation/evaluation

Fungsi:

Mengambil skor evaluasi model.

---

## 19.3 Result API

GET /api/result

Fungsi:

Mengambil hasil segmentasi pelanggan.

GET /api/result/summary

Fungsi:

Mengambil ringkasan karakteristik cluster.

---

## 19.4 Search API

GET /api/search

Parameter:

1. keyword
2. segment
3. cluster

Fungsi:

Mencari data pelanggan hasil segmentasi.

---

## 19.5 Download API

GET /api/download/csv

Fungsi:

Mengunduh hasil dalam format CSV.

GET /api/download/excel

Fungsi:

Mengunduh hasil dalam format Excel.

GET /api/download/json

Fungsi:

Mengunduh hasil dalam format JSON.

---

## 20. Kebutuhan Fungsional

| No | Kebutuhan Fungsional |
|---|---|
| 1 | Sistem dapat melakukan login Data Analyst. |
| 2 | Sistem dapat membaca data pelanggan dan transaksi yang sudah tertanam. |
| 3 | Sistem dapat menjalankan proses segmentasi melalui tombol start pipeline. |
| 4 | Sistem dapat menjalankan tahapan CRISP-DM secara end-to-end. |
| 5 | Sistem dapat melakukan data cleaning. |
| 6 | Sistem dapat menghitung fitur LRFMC. |
| 7 | Sistem dapat melakukan normalisasi data. |
| 8 | Sistem dapat menjalankan K-Means Plus. |
| 9 | Sistem dapat menghitung Elbow Method. |
| 10 | Sistem dapat menghitung Silhouette Score. |
| 11 | Sistem dapat menghitung Davies-Bouldin Index. |
| 12 | Sistem dapat menghitung Calinski-Harabasz Index. |
| 13 | Sistem dapat menampilkan hasil cluster pelanggan. |
| 14 | Sistem dapat menampilkan karakteristik cluster. |
| 15 | Sistem dapat mencari data pelanggan. |
| 16 | Sistem dapat mengunduh hasil segmentasi. |
| 17 | Sistem dapat menyimpan seluruh hasil ke MySQL. |

---

## 21. Kebutuhan Non-Fungsional

| No | Kebutuhan Non-Fungsional |
|---|---|
| 1 | Sistem dapat diakses melalui web browser. |
| 2 | Sistem memiliki antarmuka sederhana dan mudah digunakan. |
| 3 | Sistem memakai database MySQL. |
| 4 | Sistem menjalankan proses segmentasi tanpa upload manual. |
| 5 | Sistem menampilkan progress proses secara jelas. |
| 6 | Sistem menyimpan hasil secara terstruktur. |
| 7 | Sistem dapat menghasilkan file export. |
| 8 | Sistem dapat digunakan oleh Data Analyst tanpa menjalankan notebook. |

---

## 22. Alat Penelitian

| No | Alat | Spesifikasi |
|---|---|---|
| 1 | Frontend | HTML, CSS, JavaScript, dan Plotly untuk antarmuka serta visualisasi data |
| 2 | Backend | Python Flask sebagai server aplikasi dan pengelola logika bisnis |
| 3 | Machine Learning Library | scikit-learn untuk implementasi algoritma K-Means Plus |
| 4 | Framework | CRISP-DM sebagai metode end-to-end data mining |
| 5 | Database | MySQL sebagai penyimpanan data pelanggan, data transaksi, hasil LRFMC, hasil clustering, dan skor evaluasi |
| 6 | File Export | CSV, Excel, dan JSON sebagai format unduhan hasil segmentasi |

---

## 23. Acceptance Criteria

Sistem dinyatakan berhasil jika:

1. Data Analyst dapat login.
2. Sistem menolak login yang salah.
3. Sistem tidak menyediakan fitur Upload CSV.
4. Sistem tidak menyediakan fitur Create Project.
5. Sistem hanya menggunakan K-Means Plus.
6. Sistem membaca data dari MySQL.
7. Sistem menjalankan proses segmentasi dari tombol start pipeline.
8. Sistem menghitung LRFMC.
9. Sistem melakukan normalisasi data.
10. Sistem menjalankan inisialisasi centroid K-Means Plus.
11. Sistem melakukan assignment data ke centroid.
12. Sistem melakukan update centroid sampai konvergen.
13. Sistem menghitung Elbow Method.
14. Sistem menghitung Silhouette Score.
15. Sistem menghitung DBI.
16. Sistem menghitung CHI.
17. Sistem menyimpan hasil clustering ke MySQL.
18. Sistem menampilkan hasil segmentasi.
19. Sistem menampilkan grafik jumlah pelanggan per segmen.
20. Sistem dapat mencari data pelanggan.
21. Sistem dapat mengunduh hasil segmentasi.

---

## 24. Revisi Diagram yang Harus Dilakukan

Diagram yang dipertahankan:

1. Use Case Login.
2. Use Case Proses Segmentasi.
3. Use Case Lihat Hasil.
4. Use Case Search Data.
5. Use Case Download Result.
6. Activity Diagram Login.
7. Activity Diagram Proses Segmentasi.
8. Activity Diagram Lihat Hasil.
9. Activity Diagram Search Data.
10. Activity Diagram Download Result.
11. Class Diagram.
12. Sequence Diagram Proses Segmentasi.
13. Component Diagram.
14. Deployment Diagram.
15. Interface Login.
16. Interface Proses Segmentasi.
17. Interface Hasil.
18. Interface Search Data.
19. Interface Download Result.

Diagram yang harus dihapus:

1. Use Case Upload CSV.
2. Use Case Create Project.
3. Activity Diagram Upload CSV.
4. Activity Diagram Create Project.
5. Sequence Diagram Upload Dataset.
6. Sequence Diagram Create Project.
7. Communication Diagram Upload CSV.
8. Communication Diagram Create Project.
9. Interface Upload CSV.
10. Interface Create Project.

Bagian yang perlu diganti:

1. Kata upload_date diganti menjadi loaded_at.
2. Metadata project diganti menjadi metadata proses.
3. createProject() dihapus dari class Data Analyst.
4. Entity Project dihapus dari CDM, LDM, dan PDM.
5. Dataset tetap ada, tetapi artinya adalah data tertanam, bukan data upload.
6. Semua penyimpanan utama diarahkan ke MySQL.

---
````md
# Struktur Folder Sistem Segmentasi Pelanggan

Struktur folder ini dibuat untuk sistem web segmentasi pelanggan dengan ketentuan berikut:

1. Tidak ada Upload CSV.
2. Tidak ada Create Project.
3. Tidak ada K-Means klasik.
4. Algoritma hanya K-Means Plus.
5. Database menggunakan MySQL.
6. Data pelanggan dan transaksi sudah tertanam di sistem.
7. Backend menggunakan Python Flask.
8. Frontend menggunakan HTML, CSS, JavaScript, dan Plotly.
9. Machine learning menggunakan scikit-learn.
10. Framework proses menggunakan CRISP-DM.

---

# 1. Struktur Folder Utama

```txt
sistem-segmentasi-pelanggan/
│
├── backend/
│
├── frontend/
│
├── database/
│
├── data_source/
│
├── exports/
│
├── docs/
│
├── tests/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
````

---

# 2. Penjelasan Folder Utama

| Folder / File    | Fungsi                                                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| backend/         | Menyimpan seluruh kode server, API, autentikasi, proses CRISP-DM, K-Means Plus, evaluasi model, dan export hasil |
| frontend/        | Menyimpan tampilan web seperti login, proses segmentasi, hasil, search, dan download                             |
| database/        | Menyimpan skema MySQL, query pembuatan tabel, dan konfigurasi awal database                                      |
| data_source/     | Menyimpan data awal yang ditanamkan ke sistem sebelum masuk ke MySQL                                             |
| exports/         | Menyimpan file hasil segmentasi yang diunduh pengguna                                                            |
| docs/            | Menyimpan dokumentasi teknis, diagram, dan catatan pengembangan                                                  |
| tests/           | Menyimpan pengujian fungsi backend dan machine learning                                                          |
| requirements.txt | Menyimpan daftar library Python yang dibutuhkan                                                                  |
| .env             | Menyimpan konfigurasi rahasia seperti host database, user MySQL, dan secret key                                  |
| .gitignore       | Mengatur file yang tidak perlu masuk Git                                                                         |
| README.md        | Menjelaskan cara instalasi, konfigurasi, dan menjalankan sistem                                                  |

---

# 3. Struktur Folder Backend

```txt
backend/
│
├── app.py
├── config.py
│
├── routes/
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── data_routes.py
│   ├── segmentation_routes.py
│   ├── result_routes.py
│   ├── search_routes.py
│   └── download_routes.py
│
├── controllers/
│   ├── auth_controller.py
│   ├── dashboard_controller.py
│   ├── data_controller.py
│   ├── segmentation_controller.py
│   ├── result_controller.py
│   ├── search_controller.py
│   └── download_controller.py
│
├── services/
│   ├── auth_service.py
│   ├── embedded_data_service.py
│   ├── crispdm_service.py
│   ├── preprocessing_service.py
│   ├── lrfmc_service.py
│   ├── normalization_service.py
│   ├── kmeansplus_service.py
│   ├── evaluation_service.py
│   ├── result_service.py
│   ├── search_service.py
│   └── download_service.py
│
├── models/
│   ├── user_model.py
│   ├── login_model.py
│   ├── customer_model.py
│   ├── transaction_model.py
│   ├── dataset_model.py
│   ├── lrfmc_model.py
│   ├── model_result_model.py
│   ├── evaluation_model.py
│   └── cluster_result_model.py
│
├── repositories/
│   ├── user_repository.py
│   ├── customer_repository.py
│   ├── transaction_repository.py
│   ├── dataset_repository.py
│   ├── lrfmc_repository.py
│   ├── model_repository.py
│   ├── evaluation_repository.py
│   └── cluster_result_repository.py
│
├── utils/
│   ├── database.py
│   ├── response.py
│   ├── date_helper.py
│   ├── file_exporter.py
│   ├── validator.py
│   └── logger.py
│
└── middleware/
    ├── auth_middleware.py
    └── error_handler.py
```

---

# 4. Penjelasan Folder Backend

## 4.1 app.py

File utama untuk menjalankan aplikasi Flask.

Fungsi:

1. Membuat instance Flask.
2. Memuat konfigurasi sistem.
3. Mendaftarkan semua route.
4. Menjalankan server backend.

---

## 4.2 config.py

File konfigurasi sistem.

Isi utama:

1. Konfigurasi database MySQL.
2. Secret key aplikasi.
3. Path folder export.
4. Mode aplikasi, seperti development atau production.

---

## 4.3 routes/

Folder ini menyimpan endpoint API.

| File                   | Fungsi                                     |
| ---------------------- | ------------------------------------------ |
| auth_routes.py         | Mengatur endpoint login dan logout         |
| dashboard_routes.py    | Mengatur endpoint ringkasan dashboard      |
| data_routes.py         | Mengatur endpoint data tertanam            |
| segmentation_routes.py | Mengatur endpoint proses segmentasi        |
| result_routes.py       | Mengatur endpoint hasil segmentasi         |
| search_routes.py       | Mengatur endpoint pencarian data pelanggan |
| download_routes.py     | Mengatur endpoint download hasil           |

---

## 4.4 controllers/

Folder ini menjadi penghubung antara route dan service.

| File                       | Fungsi                                      |
| -------------------------- | ------------------------------------------- |
| auth_controller.py         | Mengatur alur request login                 |
| dashboard_controller.py    | Mengatur data ringkasan dashboard           |
| data_controller.py         | Mengatur preview dan validasi data tertanam |
| segmentation_controller.py | Mengatur eksekusi pipeline segmentasi       |
| result_controller.py       | Mengatur tampilan hasil cluster             |
| search_controller.py       | Mengatur pencarian pelanggan                |
| download_controller.py     | Mengatur proses unduhan file                |

---

## 4.5 services/

Folder ini menyimpan logika utama sistem.

| File                     | Fungsi                                                         |
| ------------------------ | -------------------------------------------------------------- |
| auth_service.py          | Validasi akun Data Analyst                                     |
| embedded_data_service.py | Membaca data pelanggan dan transaksi dari MySQL                |
| crispdm_service.py       | Mengatur tahapan CRISP-DM                                      |
| preprocessing_service.py | Cleaning, duplikasi, outlier, dan transformasi awal            |
| lrfmc_service.py         | Menghitung Loyalty, Recency, Frequency, Monetary, dan Category |
| normalization_service.py | Melakukan normalisasi data dengan StandardScaler               |
| kmeansplus_service.py    | Menjalankan algoritma K-Means Plus                             |
| evaluation_service.py    | Menghitung Elbow, Silhouette, DBI, dan CHI                     |
| result_service.py        | Membuat label segmen dan ringkasan cluster                     |
| search_service.py        | Mencari pelanggan dari hasil segmentasi                        |
| download_service.py      | Membuat file CSV, Excel, dan JSON                              |

---

## 4.6 models/

Folder ini mendefinisikan struktur data yang digunakan aplikasi.

| File                    | Fungsi                           |
| ----------------------- | -------------------------------- |
| user_model.py           | Struktur data Data Analyst       |
| login_model.py          | Struktur data riwayat login      |
| customer_model.py       | Struktur data pelanggan          |
| transaction_model.py    | Struktur data transaksi          |
| dataset_model.py        | Struktur metadata data tertanam  |
| lrfmc_model.py          | Struktur data hasil LRFMC        |
| model_result_model.py   | Struktur data model K-Means Plus |
| evaluation_model.py     | Struktur data evaluasi model     |
| cluster_result_model.py | Struktur data hasil cluster      |

---

## 4.7 repositories/

Folder ini menangani komunikasi langsung dengan database MySQL.

| File                         | Fungsi                      |
| ---------------------------- | --------------------------- |
| user_repository.py           | Query data user             |
| customer_repository.py       | Query data pelanggan        |
| transaction_repository.py    | Query data transaksi        |
| dataset_repository.py        | Query metadata dataset      |
| lrfmc_repository.py          | Simpan dan ambil data LRFMC |
| model_repository.py          | Simpan konfigurasi model    |
| evaluation_repository.py     | Simpan skor evaluasi        |
| cluster_result_repository.py | Simpan hasil segmentasi     |

---

## 4.8 utils/

Folder ini menyimpan fungsi bantuan.

| File             | Fungsi                             |
| ---------------- | ---------------------------------- |
| database.py      | Koneksi MySQL                      |
| response.py      | Format response API                |
| date_helper.py   | Fungsi pengolahan tanggal          |
| file_exporter.py | Fungsi export CSV, Excel, dan JSON |
| validator.py     | Validasi data                      |
| logger.py        | Pencatatan log proses              |

---

## 4.9 middleware/

Folder ini menyimpan proses tambahan sebelum atau sesudah request.

| File               | Fungsi                              |
| ------------------ | ----------------------------------- |
| auth_middleware.py | Mengecek session login Data Analyst |
| error_handler.py   | Mengatur pesan error sistem         |

---

# 5. Struktur Folder Frontend

```txt
frontend/
│
├── pages/
│   ├── login.html
│   ├── dashboard.html
│   ├── data_embedded.html
│   ├── segmentation_process.html
│   ├── result.html
│   ├── search.html
│   └── download.html
│
├── assets/
│   ├── css/
│   │   ├── global.css
│   │   ├── login.css
│   │   ├── dashboard.css
│   │   ├── process.css
│   │   ├── result.css
│   │   ├── search.css
│   │   └── download.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── dashboard.js
│   │   ├── data_embedded.js
│   │   ├── segmentation_process.js
│   │   ├── result.js
│   │   ├── search.js
│   │   ├── download.js
│   │   └── chart.js
│   │
│   └── images/
│       └── logo.png
│
└── components/
    ├── navbar.html
    ├── sidebar.html
    ├── table.html
    ├── progress_log.html
    └── evaluation_card.html
```

---

# 6. Penjelasan Folder Frontend

## 6.1 pages/

Folder ini menyimpan halaman utama sistem.

| File                      | Fungsi                                  |
| ------------------------- | --------------------------------------- |
| login.html                | Halaman autentikasi Data Analyst        |
| dashboard.html            | Halaman ringkasan sistem                |
| data_embedded.html        | Halaman preview data tertanam           |
| segmentation_process.html | Halaman start pipeline dan progress log |
| result.html               | Halaman hasil segmentasi                |
| search.html               | Halaman pencarian pelanggan             |
| download.html             | Halaman download hasil segmentasi       |

---

## 6.2 assets/css/

Folder ini menyimpan style tampilan.

| File          | Fungsi                          |
| ------------- | ------------------------------- |
| global.css    | Style umum seluruh halaman      |
| login.css     | Style halaman login             |
| dashboard.css | Style dashboard                 |
| process.css   | Style halaman proses segmentasi |
| result.css    | Style halaman hasil             |
| search.css    | Style halaman search            |
| download.css  | Style halaman download          |

---

## 6.3 assets/js/

Folder ini menyimpan logika interaksi frontend.

| File                    | Fungsi                          |
| ----------------------- | ------------------------------- |
| api.js                  | Konfigurasi pemanggilan API     |
| auth.js                 | Proses login dan logout         |
| dashboard.js            | Mengambil ringkasan dashboard   |
| data_embedded.js        | Menampilkan data tertanam       |
| segmentation_process.js | Menjalankan pipeline segmentasi |
| result.js               | Menampilkan hasil segmentasi    |
| search.js               | Menjalankan pencarian data      |
| download.js             | Menjalankan download hasil      |
| chart.js                | Menampilkan visualisasi Plotly  |

---

## 6.4 components/

Folder ini menyimpan komponen HTML yang digunakan berulang.

| File                 | Fungsi                   |
| -------------------- | ------------------------ |
| navbar.html          | Navigasi atas            |
| sidebar.html         | Menu samping             |
| table.html           | Komponen tabel           |
| progress_log.html    | Komponen progress proses |
| evaluation_card.html | Komponen skor evaluasi   |

---

# 7. Struktur Folder Database

```txt
database/
│
├── schema.sql
├── seed_users.sql
├── seed_dataset_metadata.sql
├── seed_customers.sql
├── seed_transactions.sql
├── views.sql
└── indexes.sql
```

---

# 8. Penjelasan Folder Database

| File                      | Fungsi                                 |
| ------------------------- | -------------------------------------- |
| schema.sql                | Membuat tabel utama MySQL              |
| seed_users.sql            | Mengisi akun awal Data Analyst         |
| seed_dataset_metadata.sql | Mengisi metadata data tertanam         |
| seed_customers.sql        | Mengisi data master pelanggan ke MySQL |
| seed_transactions.sql     | Mengisi data transaksi ke MySQL        |
| views.sql                 | Membuat view untuk hasil gabungan      |
| indexes.sql               | Membuat index agar query lebih cepat   |

---

# 9. Struktur Folder Data Source

```txt
data_source/
│
├── raw/
│   ├── exported_data.xlsx
│   └── exported_data_mutasi.xlsx
│
├── processed/
│   ├── customers_clean.csv
│   ├── transactions_clean.csv
│   └── lrfmc_preview.csv
│
└── loader/
    ├── load_customers.py
    ├── load_transactions.py
    └── load_to_mysql.py
```

---

# 10. Penjelasan Folder Data Source

## 10.1 raw/

Menyimpan data awal penelitian.

| File                      | Fungsi                |
| ------------------------- | --------------------- |
| exported_data.xlsx        | Data master pelanggan |
| exported_data_mutasi.xlsx | Data mutasi transaksi |

Catatan:

Folder ini hanya dipakai oleh developer untuk memasukkan data awal ke sistem. Data Analyst tidak mengunggah file dari antarmuka web.

---

## 10.2 processed/

Menyimpan hasil pembersihan awal jika diperlukan.

| File                   | Fungsi                             |
| ---------------------- | ---------------------------------- |
| customers_clean.csv    | Data pelanggan hasil cleaning awal |
| transactions_clean.csv | Data transaksi hasil cleaning awal |
| lrfmc_preview.csv      | Preview hasil transformasi LRFMC   |

---

## 10.3 loader/

Folder ini menyimpan script untuk memasukkan data ke MySQL.

| File                 | Fungsi                            |
| -------------------- | --------------------------------- |
| load_customers.py    | Membaca data master pelanggan     |
| load_transactions.py | Membaca data mutasi transaksi     |
| load_to_mysql.py     | Memasukkan data ke database MySQL |

---

# 11. Struktur Folder Exports

```txt
exports/
│
├── csv/
│   └── segmentation_result.csv
│
├── excel/
│   └── segmentation_result.xlsx
│
└── json/
    └── segmentation_result.json
```

---

# 12. Penjelasan Folder Exports

| Folder | Fungsi                                  |
| ------ | --------------------------------------- |
| csv/   | Menyimpan hasil segmentasi format CSV   |
| excel/ | Menyimpan hasil segmentasi format Excel |
| json/  | Menyimpan hasil segmentasi format JSON  |

File pada folder ini dibuat otomatis saat Data Analyst menekan tombol Download.

---

# 13. Struktur Folder Docs

```txt
docs/
│
├── prd.md
├── api_documentation.md
├── database_design.md
├── crispdm_flow.md
├── kmeansplus_flow.md
├── evaluation_metrics.md
│
└── diagrams/
    ├── use_case.png
    ├── activity_process.png
    ├── class_diagram.png
    ├── sequence_process.png
    ├── component_diagram.png
    └── deployment_diagram.png
```

---

# 14. Penjelasan Folder Docs

| File / Folder         | Fungsi                           |
| --------------------- | -------------------------------- |
| prd.md                | Dokumen kebutuhan produk         |
| api_documentation.md  | Dokumentasi endpoint API         |
| database_design.md    | Dokumentasi rancangan MySQL      |
| crispdm_flow.md       | Dokumentasi tahapan CRISP-DM     |
| kmeansplus_flow.md    | Dokumentasi alur K-Means Plus    |
| evaluation_metrics.md | Dokumentasi metrik evaluasi      |
| diagrams/             | Menyimpan seluruh diagram sistem |

---

# 15. Struktur Folder Tests

```txt
tests/
│
├── test_auth.py
├── test_data_embedded.py
├── test_lrfmc.py
├── test_kmeansplus.py
├── test_evaluation.py
├── test_result.py
├── test_search.py
└── test_download.py
```

---

# 16. Penjelasan Folder Tests

| File                  | Fungsi                                  |
| --------------------- | --------------------------------------- |
| test_auth.py          | Menguji login dan logout                |
| test_data_embedded.py | Menguji pembacaan data dari MySQL       |
| test_lrfmc.py         | Menguji perhitungan LRFMC               |
| test_kmeansplus.py    | Menguji proses K-Means Plus             |
| test_evaluation.py    | Menguji Elbow, Silhouette, DBI, dan CHI |
| test_result.py        | Menguji hasil segmentasi                |
| test_search.py        | Menguji pencarian data pelanggan        |
| test_download.py      | Menguji export file hasil               |

---

# 17. File requirements.txt

```txt
Flask
Flask-Cors
mysql-connector-python
SQLAlchemy
pandas
numpy
scikit-learn
openpyxl
python-dotenv
Werkzeug
```

---

# 18. File .env

```txt
APP_NAME=Sistem Segmentasi Pelanggan
APP_ENV=development
APP_DEBUG=True

DB_HOST=localhost
DB_PORT=3306
DB_NAME=segmentasi_pelanggan
DB_USER=root
DB_PASSWORD=

SECRET_KEY=change_this_secret_key

EXPORT_CSV_PATH=exports/csv/
EXPORT_EXCEL_PATH=exports/excel/
EXPORT_JSON_PATH=exports/json/
```

---

# 19. File README.md

Isi README.md yang disarankan:

```md
# Sistem Segmentasi Pelanggan

Sistem ini digunakan untuk melakukan segmentasi pelanggan berdasarkan nilai transaksi perusahaan menggunakan algoritma K-Means Plus dan framework CRISP-DM.

## Teknologi

- Frontend: HTML, CSS, JavaScript, Plotly
- Backend: Python Flask
- Machine Learning: scikit-learn
- Database: MySQL
- Export: CSV, Excel, JSON

## Fitur

1. Login Data Analyst
2. Proses Segmentasi
3. Lihat Hasil
4. Search Data
5. Download Result

## Catatan

Sistem tidak menggunakan Upload CSV.  
Sistem tidak menggunakan Create Project.  
Sistem tidak menggunakan K-Means klasik.  
Data pelanggan dan transaksi sudah tertanam di database MySQL.
```

---

# 20. Struktur Folder Final yang Disarankan

```txt
sistem-segmentasi-pelanggan/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── data_routes.py
│   │   ├── segmentation_routes.py
│   │   ├── result_routes.py
│   │   ├── search_routes.py
│   │   └── download_routes.py
│   │
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── dashboard_controller.py
│   │   ├── data_controller.py
│   │   ├── segmentation_controller.py
│   │   ├── result_controller.py
│   │   ├── search_controller.py
│   │   └── download_controller.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── embedded_data_service.py
│   │   ├── crispdm_service.py
│   │   ├── preprocessing_service.py
│   │   ├── lrfmc_service.py
│   │   ├── normalization_service.py
│   │   ├── kmeansplus_service.py
│   │   ├── evaluation_service.py
│   │   ├── result_service.py
│   │   ├── search_service.py
│   │   └── download_service.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── login_model.py
│   │   ├── customer_model.py
│   │   ├── transaction_model.py
│   │   ├── dataset_model.py
│   │   ├── lrfmc_model.py
│   │   ├── model_result_model.py
│   │   ├── evaluation_model.py
│   │   └── cluster_result_model.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── customer_repository.py
│   │   ├── transaction_repository.py
│   │   ├── dataset_repository.py
│   │   ├── lrfmc_repository.py
│   │   ├── model_repository.py
│   │   ├── evaluation_repository.py
│   │   └── cluster_result_repository.py
│   │
│   ├── utils/
│   │   ├── database.py
│   │   ├── response.py
│   │   ├── date_helper.py
│   │   ├── file_exporter.py
│   │   ├── validator.py
│   │   └── logger.py
│   │
│   └── middleware/
│       ├── auth_middleware.py
│       └── error_handler.py
│
├── frontend/
│   ├── pages/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── data_embedded.html
│   │   ├── segmentation_process.html
│   │   ├── result.html
│   │   ├── search.html
│   │   └── download.html
│   │
│   ├── assets/
│   │   ├── css/
│   │   │   ├── global.css
│   │   │   ├── login.css
│   │   │   ├── dashboard.css
│   │   │   ├── process.css
│   │   │   ├── result.css
│   │   │   ├── search.css
│   │   │   └── download.css
│   │   │
│   │   ├── js/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   ├── dashboard.js
│   │   │   ├── data_embedded.js
│   │   │   ├── segmentation_process.js
│   │   │   ├── result.js
│   │   │   ├── search.js
│   │   │   ├── download.js
│   │   │   └── chart.js
│   │   │
│   │   └── images/
│   │       └── logo.png
│   │
│   └── components/
│       ├── navbar.html
│       ├── sidebar.html
│       ├── table.html
│       ├── progress_log.html
│       └── evaluation_card.html
│
├── database/
│   ├── schema.sql
│   ├── seed_users.sql
│   ├── seed_dataset_metadata.sql
│   ├── seed_customers.sql
│   ├── seed_transactions.sql
│   ├── views.sql
│   └── indexes.sql
│
├── data_source/
│   ├── raw/
│   │   ├── exported_data.xlsx
│   │   └── exported_data_mutasi.xlsx
│   │
│   ├── processed/
│   │   ├── customers_clean.csv
│   │   ├── transactions_clean.csv
│   │   └── lrfmc_preview.csv
│   │
│   └── loader/
│       ├── load_customers.py
│       ├── load_transactions.py
│       └── load_to_mysql.py
│
├── exports/
│   ├── csv/
│   │   └── segmentation_result.csv
│   │
│   ├── excel/
│   │   └── segmentation_result.xlsx
│   │
│   └── json/
│       └── segmentation_result.json
│
├── docs/
│   ├── prd.md
│   ├── api_documentation.md
│   ├── database_design.md
│   ├── crispdm_flow.md
│   ├── kmeansplus_flow.md
│   ├── evaluation_metrics.md
│   │
│   └── diagrams/
│       ├── use_case.png
│       ├── activity_process.png
│       ├── class_diagram.png
│       ├── sequence_process.png
│       ├── component_diagram.png
│       └── deployment_diagram.png
│
├── tests/
│   ├── test_auth.py
│   ├── test_data_embedded.py
│   ├── test_lrfmc.py
│   ├── test_kmeansplus.py
│   ├── test_evaluation.py
│   ├── test_result.py
│   ├── test_search.py
│   └── test_download.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 21. Alur Kerja Folder Saat Sistem Berjalan

1. Data awal berada di `data_source/raw/`.
2. Developer menjalankan script loader di `data_source/loader/`.
3. Data masuk ke MySQL melalui file di `database/`.
4. Data Analyst login melalui halaman `frontend/pages/login.html`.
5. Frontend mengirim request ke `backend/routes/auth_routes.py`.
6. Sistem memvalidasi akun melalui `auth_service.py`.
7. Data Analyst membuka halaman proses segmentasi.
8. Request masuk ke `segmentation_routes.py`.
9. Controller memanggil `segmentation_controller.py`.
10. Service utama menjalankan `crispdm_service.py`.
11. Data dibaca oleh `embedded_data_service.py`.
12. Data diproses oleh `preprocessing_service.py`.
13. Fitur LRFMC dihitung oleh `lrfmc_service.py`.
14. Data dinormalisasi oleh `normalization_service.py`.
15. K-Means Plus dijalankan oleh `kmeansplus_service.py`.
16. Evaluasi dihitung oleh `evaluation_service.py`.
17. Hasil disimpan melalui repository ke MySQL.
18. Halaman result mengambil data dari `result_routes.py`.
19. Search dijalankan melalui `search_routes.py`.
20. Download dijalankan melalui `download_routes.py`.
21. File hasil dibuat di folder `exports/`.

---

# 22. Catatan Revisi dari Diagram

Struktur folder ini sudah menyesuaikan perubahan berikut:

1. Tidak ada folder upload.
2. Tidak ada route upload.
3. Tidak ada controller upload.
4. Tidak ada service upload.
5. Tidak ada halaman upload CSV.
6. Tidak ada create_project route.
7. Tidak ada create_project controller.
8. Tidak ada create_project service.
9. Tidak ada model project.
10. Tidak ada repository project.
11. Tidak ada service K-Means klasik.
12. Model clustering hanya `kmeansplus_service.py`.
13. Database utama menggunakan MySQL.
14. Dataset tetap ada, tetapi sebagai data tertanam.
15. Kolom `upload_date` diganti menjadi `loaded_at`.

```
```

## 25. Narasi Untuk Laporan

Sistem Segmentasi Pelanggan merupakan aplikasi web yang dirancang untuk membantu Data Analyst menjalankan proses segmentasi pelanggan berdasarkan nilai transaksi perusahaan. Sistem ini menggunakan data pelanggan dan data mutasi transaksi yang sudah tertanam di dalam database MySQL, sehingga pengguna tidak perlu melakukan upload data secara manual. Proses segmentasi dijalankan melalui tombol start pipeline pada halaman Proses Segmentasi.

Alur sistem mengikuti framework CRISP-DM yang terdiri dari Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, dan Deployment. Pada tahap Data Preparation, sistem membersihkan data, menghapus duplikasi, menghitung fitur LRFMC, dan melakukan normalisasi data. Pada tahap Modeling, sistem menjalankan algoritma K-Means Plus untuk membentuk cluster pelanggan. Proses K-Means Plus dimulai dari pemilihan centroid awal, perhitungan jarak D(x)², perhitungan probabilitas P(x), pemilihan centroid berikutnya, assignment data ke centroid, update centroid, dan pengecekan konvergensi.

Pada tahap Evaluation, sistem menghitung Elbow Method, Silhouette Score, Davies-Bouldin Index, dan Calinski-Harabasz Index untuk menilai kualitas cluster. Hasil akhir proses disimpan ke database MySQL dan ditampilkan pada halaman Lihat Hasil. Data Analyst dapat melihat grafik jumlah pelanggan per segmen, karakteristik cluster, dan tabel hasil pelanggan. Sistem juga menyediakan fitur Search Data untuk mencari pelanggan tertentu serta fitur Download Result untuk mengunduh hasil segmentasi dalam format CSV, Excel, atau JSON.

Dengan rancangan ini, proses segmentasi pelanggan menjadi lebih terarah, terdokumentasi, dan mudah digunakan. Sistem tidak lagi bergantung pada eksekusi notebook manual karena seluruh tahapan analisis telah diintegrasikan ke dalam aplikasi web.