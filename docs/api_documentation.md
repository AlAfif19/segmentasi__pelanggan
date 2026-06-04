# API Documentation

Base URL: `/api`

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| GET | `/health` | Mengecek status aplikasi |
| POST | `/auth/login` | Login Data Analyst |
| POST | `/auth/logout` | Logout |
| GET | `/dashboard/` | Ringkasan data dan evaluasi |
| GET | `/data/embedded` | Preview data tertanam |
| POST | `/segmentation/run` | Menjalankan pipeline CRISP-DM dan K-Means Plus |
| GET | `/result/` | Mengambil hasil segmentasi |
| GET | `/search/?keyword=Adi&category=name&segment=all` | Mencari data pelanggan |
| POST | `/download/` | Membuat file export hasil |

Catatan: endpoint membaca data dari MySQL. Jika database belum aktif atau hasil segmentasi belum tersedia, API mengembalikan data kosong dan status yang sesuai.
