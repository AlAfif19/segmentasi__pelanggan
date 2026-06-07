# Desain Loyalty Fallback dan Scaler Global

## Tujuan

Menghasilkan fitur Loyalty yang informatif saat CSV tidak memiliki tanggal aktif,
serta menggunakan satu scaler yang konsisten untuk seluruh periode segmentasi.

## Definisi Loyalty

Sumber Loyalty dipilih per pelanggan:

1. Jika `active_date` tersedia, Loyalty adalah selisih tanggal analisis dengan
   tanggal aktif.
2. Jika `active_date` kosong, Loyalty adalah selisih transaksi pembayaran
   relevan terakhir dengan transaksi pembayaran relevan pertama.
3. Jika pelanggan hanya memiliki satu transaksi relevan atau tidak memiliki
   transaksi relevan, Loyalty bernilai nol.

Transaksi relevan memiliki `money_in > 0`, tanggal valid, customer ID yang
terhubung, dan jenis transaksi mengandung `TAGIHAN`, `PEMBAYARAN`, atau `BAYAR`.

Fallback Loyalty dihitung dari seluruh riwayat transaksi sampai tanggal analisis,
bukan dari jendela periode segmentasi. Dengan demikian nilai Loyalty pelanggan
tidak berubah ketika pengguna memilih periode 1, 3, atau 6 bulan.

## Perbandingan Scaler

Perbandingan awal hanya menggunakan dua konfigurasi:

- `logfm_standard`: transformasi `log1p` pada Frequency dan Monetary,
  winsorization 1%, lalu `StandardScaler`.
- `logfm_robust`: transformasi `log1p` pada Frequency dan Monetary,
  winsorization 1%, lalu `RobustScaler`.

Kedua konfigurasi diuji pada periode 1 bulan, 3 bulan, 6 bulan, dan 1 tahun.
Periode semua data tidak ikut menentukan pemenang karena dataset saat ini identik
dengan periode 1 tahun.

Untuk setiap periode dan scaler, sistem mencari K melalui elbow dan mencatat
Silhouette, Davies-Bouldin, dan Calinski-Harabasz. Setiap metrik dinormalisasi
antar-scaler per periode. Skor periode menggunakan bobot:

- Silhouette lebih tinggi: 45%
- Davies-Bouldin lebih rendah: 35%
- Calinski-Harabasz lebih tinggi: 20%

Scaler dengan rata-rata skor periode tertinggi menjadi scaler global. Jika skor
sama, prioritas berurutan adalah rata-rata Silhouette lebih tinggi, rata-rata DBI
lebih rendah, kemudian `StandardScaler` untuk hasil yang deterministik.

## Model Produksi

Setelah scaler global dipilih, pipeline produksi hanya menggunakan konfigurasi
tersebut pada semua periode. K optimal tetap boleh berbeda per periode karena
struktur data transaksi berbeda, tetapi transformasi, winsorization, dan scaler
harus sama.

Nama konfigurasi, transformasi, winsorization, scaler, dan K optimal ditampilkan
dan dicatat dalam hasil benchmark.

## Pengujian

Tes unit memverifikasi prioritas `active_date`, fallback transaksi, satu transaksi,
tanpa transaksi, dan bahwa fallback tidak berubah terhadap filter periode.

Evaluasi scaler menghasilkan laporan CSV/Markdown yang memuat semua metrik,
skor global, dan alasan pemilihan. Setelah konfigurasi dikunci, benchmark browser
dijalankan lima kali untuk setiap periode dan mengganti laporan benchmark lama.
