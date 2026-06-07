# Loader Dua Format dan Benchmark Segmentasi Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mendukung CSV/XLSX pelanggan, filter periode segmentasi, dan benchmark black-box browser yang menghasilkan data penelitian.

**Architecture:** Loader menormalisasi kedua format menjadi lima kolom internal. Controller memvalidasi kode periode lalu repository menerapkan batas tanggal pada seluruh agregasi transaksi. UI mengirim periode terpilih, sedangkan Playwright mengukur waktu dari klik sampai status selesai.

**Tech Stack:** Python 3.13, pandas, Flask, MySQL, React/Vite, pytest, Playwright.

---

### Task 1: Loader Pelanggan Dua Format

**Files:**
- Modify: `data_source/loader/load_customers.py`
- Modify: `data_source/loader/load_to_mysql.py`
- Create: `tests/test_customer_loader.py`

- [ ] Tulis tes pemilihan file terbaru, parsing CSV `sep=,`, pembersihan nilai `="..."`, pemetaan CSV, pemetaan XLSX, dan validasi kolom.
- [ ] Jalankan `python -m pytest tests/test_customer_loader.py -v` dan pastikan gagal karena API loader belum tersedia.
- [ ] Implementasikan `find_customer_file`, pembaca berdasarkan ekstensi, normalisasi kolom, dan metadata sumber.
- [ ] Ubah pencatatan dataset agar memakai nama file sumber aktual.
- [ ] Jalankan tes loader sampai lulus.

### Task 2: Filter Periode Segmentasi

**Files:**
- Modify: `backend/controllers/segmentation_controller.py`
- Modify: `backend/services/crispdm_service.py`
- Modify: `backend/repositories/mysql_repository.py`
- Create: `tests/test_segmentation_period.py`

- [ ] Tulis tes kode periode valid, kode tidak valid, batas tanggal kalender, dan penerusan parameter ke pipeline.
- [ ] Jalankan tes dan pastikan gagal karena filter belum tersedia.
- [ ] Tambahkan resolver periode dengan tanggal analisis maksimum 7 Juni 2026 atau tanggal hari ini, mana yang lebih awal.
- [ ] Tambahkan parameter tanggal ke query agregasi LRFMC dan statistik transaksi.
- [ ] Kembalikan metadata periode, jumlah transaksi, dan transaksi relevan.
- [ ] Jalankan tes periode dan smoke test.

### Task 3: Pilihan Periode Pada UI

**Files:**
- Modify: `src/main.jsx`

- [ ] Tambahkan state dan dropdown periode pada halaman Proses Segmentasi.
- [ ] Kirim kode periode pada `POST /api/segmentation/run`.
- [ ] Tampilkan batas tanggal, jumlah transaksi, dan durasi proses pada hasil.
- [ ] Tambahkan atribut aksesibel stabil untuk otomasi browser.
- [ ] Jalankan `npm run build`.

### Task 4: Benchmark Black-Box

**Files:**
- Modify: `package.json`
- Create: `tests/blackbox/segmentation-benchmark.mjs`
- Create: `docs/research/benchmark-segmentasi.csv`
- Create: `docs/research/benchmark-segmentasi-summary.csv`
- Create: `docs/research/benchmark-segmentasi.md`

- [ ] Pasang Playwright dan Chromium bila belum tersedia.
- [ ] Buat skrip login, navigasi, pemilihan periode, klik proses, tunggu selesai, dan pencatatan lima pengulangan.
- [ ] Jalankan backend dan frontend lokal.
- [ ] Muat data ke MySQL, lalu jalankan benchmark lima periode.
- [ ] Validasi total segmen, metrik model, filter tanggal, dan download melalui UI.
- [ ] Simpan hasil mentah, ringkasan statistik, lingkungan uji, temuan, serta keterbatasan penelitian.

### Task 5: Verifikasi Akhir

**Files:**
- Verify all modified files.

- [ ] Jalankan seluruh `pytest`.
- [ ] Jalankan build frontend.
- [ ] Jalankan loader terhadap CSV aktual.
- [ ] Jalankan satu smoke test browser setelah benchmark.
- [ ] Periksa laporan agar tidak memiliki nilai kosong yang seharusnya tersedia.
