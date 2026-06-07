# Desain Tabel Jejak K-Means Aktual

## Tujuan

Menambahkan bukti perhitungan yang dapat direproduksi untuk probabilitas
inisialisasi K-Means++, assignment 20 pelanggan, dan update centroid pada
hasil segmentasi aktual.

## Sumber Data dan Konfigurasi

- Database aktual berisi 519 pelanggan.
- Periode analisis menggunakan seluruh data sampai 7 Juni 2026.
- Fitur model adalah Loyalty, Recency, Frequency, Monetary, dan Category.
- Frequency dan Monetary ditransformasi dengan `log1p`.
- Setiap fitur diwinsorisasi 1% dan distandardisasi dengan StandardScaler.
- Model final menggunakan K=4, `random_state=42`, dan `n_init=30`.

## Tabel Probabilitas

Probabilitas direproduksi dari satu proses inisialisasi K-Means++ dengan
`random_state=42`. Centroid pertama dipilih sesuai generator acak, kemudian
setiap tahap berikutnya menampilkan pelanggan yang dipilih, nilai D(x) kuadrat,
dan probabilitasnya terhadap total D(x) kuadrat saat itu. Tabel diberi catatan
bahwa jejak ini merupakan satu inisialisasi yang dapat direproduksi, bukan
rekaman internal seluruh 30 inisialisasi scikit-learn.

## Tabel Assignment

Tabel memuat 20 pelanggan aktual pertama berdasarkan nomor pelanggan. Jarak ke
empat centroid akhir dihitung pada ruang model setelah transformasi,
winsorization, dan StandardScaler. Kolom LRFMC tetap ditampilkan dalam satuan
bisnis, sedangkan cluster terdekat mengikuti jarak minimum pada ruang model.

## Tabel Update Centroid

Tabel menampilkan centroid akhir setiap cluster sebagai rata-rata LRFMC mentah
anggota cluster. Nilai ini digunakan untuk interpretasi bisnis, sedangkan
assignment model tetap dilakukan pada ruang terstandardisasi. Jumlah pelanggan
dan label segmen harus sama dengan hasil model aktual.

## Verifikasi

- K=4, iterasi=4, dan SSE sekitar 295,695848.
- Jumlah anggota cluster adalah 83, 83, 344, dan 9.
- Setiap baris assignment memilih cluster dengan jarak minimum.
- Identitas pelanggan dan nilai LRFMC berasal dari database aktual.
