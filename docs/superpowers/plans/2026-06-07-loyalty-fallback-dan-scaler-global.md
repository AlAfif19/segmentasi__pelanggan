# Loyalty Fallback dan Scaler Global Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Menghitung Loyalty dari tanggal aktif atau rentang transaksi dan mengunci satu scaler global berdasarkan evaluasi lintas periode.

**Architecture:** Repository mengembalikan tanggal transaksi relevan pertama/terakhir dari seluruh riwayat sampai tanggal analisis, terpisah dari agregasi RFMC yang mengikuti periode. Service memilih sumber Loyalty per pelanggan. Skrip evaluasi membandingkan StandardScaler dan RobustScaler secara terkontrol, lalu konstanta konfigurasi produksi dikunci ke pemenang.

**Tech Stack:** Python, MySQL, pandas, NumPy, scikit-learn, pytest, Flask, Playwright.

---

### Task 1: Loyalty Fallback

**Files:**
- Modify: `backend/repositories/mysql_repository.py`
- Modify: `backend/services/crispdm_service.py`
- Create: `tests/test_loyalty_fallback.py`

- [ ] Tulis tes prioritas tanggal aktif, fallback rentang transaksi, satu transaksi, tanpa transaksi, dan independensi dari periode.
- [ ] Jalankan tes dan pastikan gagal karena kolom fallback belum tersedia.
- [ ] Tambahkan `first_transaction` dan `last_transaction_all` pada query sumber menggunakan subquery seluruh riwayat sampai tanggal analisis.
- [ ] Implementasikan helper pemilihan Loyalty dan metadata sumber.
- [ ] Jalankan tes sampai lulus.

### Task 2: Evaluasi Scaler Global

**Files:**
- Modify: `backend/services/crispdm_service.py`
- Create: `scripts/evaluate_scalers.py`
- Create: `tests/test_scaler_selection.py`
- Create: `docs/research/scaler-comparison.csv`
- Create: `docs/research/scaler-comparison.md`

- [ ] Ekstrak evaluasi satu konfigurasi menjadi helper yang dapat diuji.
- [ ] Tulis tes agregasi skor dan tie-break.
- [ ] Jalankan pembanding StandardScaler dan RobustScaler pada empat periode.
- [ ] Simpan metrik dan pemenang global.

### Task 3: Kunci Konfigurasi Produksi

**Files:**
- Modify: `backend/services/crispdm_service.py`
- Modify: `README.md`

- [ ] Tetapkan transformasi `log1p`, winsor 1%, dan scaler pemenang sebagai konfigurasi tunggal.
- [ ] Pastikan API tetap mengembalikan `model_config` dan `model_candidates`.
- [ ] Perbarui dokumentasi definisi Loyalty dan scaler.
- [ ] Jalankan seluruh tes backend.

### Task 4: Benchmark Ulang

**Files:**
- Modify: `tests/blackbox/segmentation-benchmark.mjs`
- Replace: `docs/research/benchmark-segmentasi.csv`
- Replace: `docs/research/benchmark-segmentasi-summary.csv`
- Replace: `docs/research/benchmark-segmentasi.md`

- [ ] Muat ulang data sumber.
- [ ] Jalankan backend dengan satu thread numerik dan frontend.
- [ ] Jalankan 25 percobaan black-box.
- [ ] Validasi total segmen, metrik, sumber Loyalty, scaler, halaman hasil, dan unduhan.
- [ ] Catat perbandingan metodologi baru.

### Task 5: Verifikasi dan Publikasi

**Files:**
- Verify all modified files.

- [ ] Jalankan seluruh pytest dan build frontend.
- [ ] Periksa diff dan file sensitif.
- [ ] Commit perubahan.
- [ ] Push ke `origin/master`.
