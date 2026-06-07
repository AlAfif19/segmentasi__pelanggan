# Desain Loader Dua Format dan Benchmark Segmentasi

## Tujuan

Sistem menerima data pelanggan dari CSV terbaru maupun XLSX lama, kemudian
menjalankan dan mengukur segmentasi melalui antarmuka web untuk periode 1 bulan,
3 bulan, 6 bulan, 1 tahun, dan semua data sampai tanggal analisis 7 Juni 2026.

## Loader Pelanggan

Loader mencari `data_source/raw/exported_data.csv` dan
`data_source/raw/exported_data.xlsx`. Jika keduanya tersedia, file dengan waktu
modifikasi paling baru dipakai agar sumber terbaru menjadi acuan. Format selain
CSV dan XLSX ditolak dengan pesan yang menjelaskan format yang didukung.

CSV dibaca dengan melewati deklarasi `sep=,` pada baris pertama. Nilai ekspor
Excel seperti `="10337831"` dibersihkan menjadi `10337831`. Pemetaan CSV:

| CSV terbaru | Kolom internal |
| --- | --- |
| `No Pelanggan` | `customer_id` |
| `Nama` | `name` |
| `Paket` | `category` |
| `Total` | `monthly_fee` |

CSV terbaru tidak memiliki tanggal aktivasi. `active_date` diisi `NULL`;
`Masa Aktif`, `Jatuh Tempo`, dan `Suspend` tidak digunakan sebagai pengganti
karena maknanya berbeda.

Pemetaan XLSX lama tetap:

| XLSX lama | Kolom internal |
| --- | --- |
| `NOPEL` | `customer_id` |
| `NAMA PELANGGAN` | `name` |
| `TGL AKTIF` | `active_date` |
| `PAKET` | `category` |
| `TOTAL TARIF` | `monthly_fee` |

Loader memvalidasi kolom wajib, menormalkan tanggal dan angka, dan mencatat nama
file sumber sebenarnya pada tabel `datasets`.

## Periode Segmentasi

Halaman Proses Segmentasi menyediakan pilihan:

- 1 bulan: 7 Mei 2026 sampai 7 Juni 2026
- 3 bulan: 7 Maret 2026 sampai 7 Juni 2026
- 6 bulan: 7 Desember 2025 sampai 7 Juni 2026
- 1 tahun: 7 Juni 2025 sampai 7 Juni 2026
- Semua data: tanggal transaksi paling awal sampai 7 Juni 2026

Kedua batas tanggal bersifat inklusif dan batas awal dihitung dengan pengurangan
bulan kalender dari tanggal akhir. Transaksi setelah 7 Juni 2026 tidak disertakan.
Backend menerapkan filter periode sebelum agregasi frequency, monetary, dan
last transaction. Pilihan periode dan batas tanggal dikirim dari web ke endpoint
segmentasi dan dicatat bersama hasil eksperimen.

## Pengujian Black-Box

Pengujian bertindak seperti pengguna:

1. Membuka web pada browser.
2. Login sebagai Data Analyst.
3. Membuka halaman Proses Segmentasi.
4. Memilih periode.
5. Menekan `Mulai Proses`.
6. Menunggu status `Segmentasi selesai`.
7. Membuka hasil dan memeriksa ringkasan serta distribusi segmen.

Waktu end-to-end dimulai tepat sebelum klik `Mulai Proses` dan berhenti setelah
status selesai terlihat pada UI. Setiap periode dijalankan lima kali. Browser
dan backend tetap berjalan, sedangkan hasil segmentasi sebelumnya boleh ditimpa
seperti perilaku aplikasi normal.

## Data Yang Dicatat

Setiap percobaan mencatat:

- nomor percobaan dan periode;
- tanggal mulai dan akhir filter;
- jumlah transaksi dalam periode;
- jumlah transaksi relevan;
- jumlah pelanggan yang diproses;
- durasi end-to-end dalam detik;
- K optimal dan jumlah iterasi;
- inertia/SSE, Silhouette, Davies-Bouldin, dan Calinski-Harabasz;
- jumlah anggota setiap segmen;
- status berhasil atau pesan kesalahan.

Rekap per periode memuat minimum, maksimum, rata-rata, median, dan simpangan baku
durasi. Hasil mentah dan rekap disimpan dalam CSV agar dapat dipakai sebagai
lampiran dan bahan analisis skripsi.

## Validasi Kebenaran

Pengujian memeriksa bahwa seluruh transaksi yang digunakan berada dalam batas
periode, jumlah pelanggan hasil sama dengan jumlah pelanggan yang diproses,
jumlah anggota segmen menjumlah ke total hasil, metrik evaluasi berupa angka
valid, dan hasil dapat dibuka serta diunduh dari web.

CSV terbaru tidak menyediakan `active_date`. Implementasi lanjutan menggunakan
rentang transaksi pembayaran relevan pertama sampai terakhir sebagai fallback
Loyalty, sedangkan XLSX yang memiliki tanggal aktivasi tetap memakai tanggal aktif.

## Strategi Otomasi

Playwright digunakan untuk mengendalikan browser lokal melalui UI. Otomasi ini
tetap merupakan pengujian black-box karena berinteraksi dengan elemen yang sama
seperti pengguna dan tidak memanggil fungsi segmentasi secara langsung.
Pengujian unit dan API tetap digunakan secara terpisah untuk memastikan filter
periode dan loader benar sebelum benchmark end-to-end dijalankan.
