# Hasil Benchmark Black-Box Segmentasi

Tanggal pengujian: 2026-06-07T07:15:46.320Z
Lingkungan: win32 10.0.19045, Intel(R) Core(TM) i5-2520M CPU @ 2.50GHz, RAM 12 GB
Browser: Playwright Chromium headless
Pengulangan: 5 kali per periode
Definisi waktu: sesaat sebelum klik Start Pipeline sampai status Segmentasi selesai terlihat di UI.

| Periode | Transaksi | Relevan | Pelanggan | Rata-rata (s) | Median (s) | Min (s) | Maks (s) | SD (s) | K | Silhouette | DBI | CHI | Validasi |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 bulan | 507 | 425 | 519 | 6.848 | 6.853 | 6.401 | 7.085 | 0.244 | 5 | 0.8147 | 0.3847 | 1459.75 | PASS |
| 3 bulan | 1417 | 1180 | 519 | 7.438 | 7.271 | 6.771 | 8.650 | 0.659 | 4 | 0.7699 | 0.4346 | 1364.47 | PASS |
| 6 bulan | 2742 | 2250 | 519 | 7.666 | 7.376 | 7.246 | 8.722 | 0.543 | 5 | 0.7011 | 0.4771 | 1191.01 | PASS |
| 1 tahun | 4774 | 3812 | 519 | 7.430 | 7.218 | 7.149 | 7.869 | 0.299 | 5 | 0.7362 | 0.4528 | 1748.80 | PASS |
| Semua data | 4774 | 3812 | 519 | 7.979 | 7.728 | 7.306 | 8.984 | 0.578 | 5 | 0.7362 | 0.4528 | 1748.80 | PASS |

## Catatan Metodologi

- Pengujian berinteraksi melalui halaman login, navigasi, dropdown periode, tombol proses, status UI, halaman hasil, dan tombol unduh.
- Tanggal akhir dibatasi sampai 7 Juni 2026. Transaksi setelah tanggal tersebut tidak digunakan.
- Backend benchmark dijalankan dengan `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, dan `MKL_NUM_THREADS=1` agar penggunaan thread numerik konsisten.
- Data transaksi aktual dimulai 6 Juli 2025, sehingga periode 1 tahun dan semua data menggunakan baris yang sama.
- CSV pelanggan tidak memiliki tanggal aktif, sehingga komponen Loyalty bernilai default nol.
- File CSV mentah dan ringkasan statistik disimpan di folder yang sama.
