# Hasil Benchmark Black-Box Segmentasi

Tanggal pengujian: 2026-06-07T07:55:04.726Z
Lingkungan: win32 10.0.19045, Intel(R) Core(TM) i5-2520M CPU @ 2.50GHz, RAM 12 GB
Browser: Playwright Chromium headless
Pengulangan: 5 kali per periode
Definisi waktu: sesaat sebelum klik Start Pipeline sampai status Segmentasi selesai terlihat di UI.

| Periode | Transaksi | Relevan | Pelanggan | Rata-rata (s) | Median (s) | Min (s) | Maks (s) | SD (s) | Scaler | K | Silhouette | DBI | CHI | Validasi |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 bulan | 507 | 425 | 519 | 5.168 | 4.033 | 3.380 | 9.832 | 2.373 | StandardScaler | 4 | 0.5174 | 0.7350 | 706.31 | PASS |
| 3 bulan | 1417 | 1180 | 519 | 5.119 | 4.377 | 4.163 | 7.936 | 1.435 | StandardScaler | 4 | 0.6009 | 0.5787 | 1074.82 | PASS |
| 6 bulan | 2742 | 2250 | 519 | 5.858 | 5.378 | 4.059 | 9.577 | 1.970 | StandardScaler | 4 | 0.6686 | 0.5069 | 1255.23 | PASS |
| 1 tahun | 4774 | 3812 | 519 | 4.149 | 4.105 | 3.158 | 6.045 | 1.026 | StandardScaler | 4 | 0.6965 | 0.4557 | 1334.86 | PASS |
| Semua data | 4774 | 3812 | 519 | 3.705 | 3.942 | 2.789 | 4.179 | 0.501 | StandardScaler | 4 | 0.6965 | 0.4557 | 1334.86 | PASS |

## Catatan Metodologi

- Pengujian berinteraksi melalui halaman login, navigasi, dropdown periode, tombol proses, status UI, halaman hasil, dan tombol unduh.
- Tanggal akhir dibatasi sampai 7 Juni 2026. Transaksi setelah tanggal tersebut tidak digunakan.
- Backend benchmark dijalankan dengan OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, dan MKL_NUM_THREADS=1 agar penggunaan thread numerik konsisten.
- Data transaksi aktual dimulai 6 Juli 2025, sehingga periode 1 tahun dan semua data menggunakan baris yang sama.
- CSV pelanggan tidak memiliki tanggal aktif; Loyalty memakai rentang transaksi pembayaran relevan pertama sampai terakhir.
- Loyalty fallback tersedia untuk 430 pelanggan; 89 pelanggan tanpa riwayat relevan bernilai nol. Rata-rata Loyalty 201,75 hari dengan rentang 0-336 hari.
- Model produksi memakai log1p Frequency/Monetary, winsorization 1%, dan StandardScaler secara konsisten.
- File CSV mentah dan ringkasan statistik disimpan di folder yang sama.
