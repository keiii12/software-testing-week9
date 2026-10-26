# Laporan Tugas Sesi 9 — Unit Testing PyTest

**Mata Kuliah:** Software Testing  
**Topik:** Unit Test PyTest dengan Fixture, Parametrize (BVA), Mocking, dan Branch Coverage  
**Studi Kasus:** Sistem Pemesanan Tiket Konser K-Pop (*"K-Pop World Tour Fest"*)

---

## 1. Deskripsi Modul Program (`kpop_concert.py`)

Modul ini memodelkan sistem transaksi tiket konser K-Pop resmi dengan 3 fungsi berlogika bersyarat:

1. **`hitung_harga_tiket(kategori, jumlah_tiket, membership=False)`**
   - Logika: Menghitung total harga tiket berdasarkan kategori (`VIP_SOUNDCHECK`, `CAT_1_FESTIVAL`, `CAT_2_SEATED`), jumlah pembelian (kuota 1–4 tiket per akun), dan status kepemilikan Global Fanclub Membership.
   - Aturan Diskon:
     - Member: beli $\ge 3$ tiket diskon 10%, beli $1-2$ tiket diskon 5%.
     - Non-Member: beli 4 tiket (bundle) diskon 2%, beli $< 4$ tiket diskon 0%.
   - Validasi: Melempar `ValueError` jika jumlah tiket $< 1$, $> 4$, atau kategori tidak valid.

2. **`validasi_penonton(usia, kategori, surat_izin=False)`**
   - Logika: Menerapkan regulasi keselamatan venue konser K-Pop.
   - Area Festival/Standing: Dilarang untuk anak $< 12$ tahun. Usia $12-16$ tahun wajib memiliki surat izin wali. Usia $\ge 17$ tahun lolos bebas.
   - Area Seated (Duduk): Dilarang untuk anak $< 7$ tahun. Usia $\ge 7$ tahun lolos.
   - Validasi: Melempar `PermissionError` atau `ValueError` jika batas dilanggar.

3. **`proses_booking_tiket(booking_id, nama_pemesan, email, usia, kategori, jumlah_tiket, membership, surat_izin)`**
   - Logika: Orkestrasi alur pemesanan lengkap, memvalidasi identitas, memeriksa kelayakan penonton, menghitung harga tiket, dan memanggil fungsi eksternal `kirim_notifikasi_eticket` untuk menerbitkan E-Ticket.
   - Isolasi Pengujian: Menggunakan Mock untuk mensimulasikan status pengiriman gateway (berhasil, gagal, atau timeout).

---

## 2. Implementasi Pengujian (`test_kpop_concert.py`)

Seluruh kriteria penilaian Sesi 9 telah dipenuhi secara lengkap:

| Kriteria Tugas Sesi 9 | Implementasi pada Kode Test | Keterangan |
| :--- | :--- | :--- |
| **(1) Minimal 8 test & 1 Parametrize berbasis BVA** | `@pytest.mark.parametrize` dengan 4 titik uji BVA ($1, 2, 3, 4$ tiket) + total 22 test case. | **Lolos (22/8 test)** |
| **(2) Minimal 2 test `pytest.raises` skenario negatif** | Diuji 8 skenario negatif (kuota $<1$, kuota $>4$, kategori salah, usia anak festival, tanpa surat izin, balita, dsb). | **Lolos (8/2 test)** |
| **(3) Minimal 1 Fixture dengan `yield` & 1 Mocking** | Fixture `antrean_booking_session` dengan setup & cleanup `yield`. Mocking `patch("kpop_concert.kirim_notifikasi_eticket")`. | **Lolos** |
| **(4) Laporan Coverage `--cov --cov-branch`** | `pytest --cov=kpop_concert --cov-branch --cov-report=term-missing` | **100% Coverage (30/30 Branch)** |

---

## 3. Cara Menjalankan Test

Jalankan perintah berikut di terminal:

```bash
# Menjalankan seluruh test dengan rincian per kasus
python -m pytest -v

# Menjalankan pengujian sekaligus menghasilkan laporan statement & branch coverage
python -m pytest -v --cov=kpop_concert --cov-branch --cov-report=term-missing --cov-report=html
```

---

## 4. Hasil Eksekusi & Laporan Coverage

```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Azzahra\Documents\College\Semester 5\software testing\week 9
plugins: cov-7.1.0
collected 22 items

test_kpop_concert.py::test_fixture_setup_dan_cleanup PASSED              [  4%]
test_kpop_concert.py::test_bva_hitung_harga_tiket_member[1-0.05-Batas bawah valid (1 tiket) -> Diskon Member 5%] PASSED [  9%]
test_kpop_concert.py::test_bva_hitung_harga_tiket_member[2-0.05-Titik batas sebelum naik tier (2 tiket) -> Diskon Member 5%] PASSED [ 13%]
test_kpop_concert.py::test_bva_hitung_harga_tiket_member[3-0.1-Titik batas awal tier diskon besar (3 tiket) -> Diskon Member 10%] PASSED [ 18%]
test_kpop_concert.py::test_bva_hitung_harga_tiket_member[4-0.1-Batas atas valid kuota war tiket (4 tiket) -> Diskon Member 10%] PASSED [ 22%]
test_kpop_concert.py::test_hitung_harga_non_member_tanpa_diskon PASSED   [ 27%]
test_kpop_concert.py::test_hitung_harga_non_member_bundle_diskon PASSED  [ 31%]
test_kpop_concert.py::test_hitung_harga_tiket_jumlah_kurang_dari_satu_raises PASSED [ 36%]
test_kpop_concert.py::test_hitung_harga_tiket_melebihi_kuota_war_raises PASSED [ 40%]
test_kpop_concert.py::test_hitung_harga_kategori_tidak_valid_raises PASSED [ 45%]
test_kpop_concert.py::test_validasi_penonton_standing_di_bawah_12_tahun_raises PASSED [ 50%]
test_kpop_concert.py::test_validasi_penonton_remaja_tanpa_surat_izin_raises PASSED [ 54%]
test_kpop_concert.py::test_validasi_penonton_balita_di_venue_raises PASSED [ 59%]
test_kpop_concert.py::test_validasi_penonton_usia_tidak_wajar_raises PASSED [ 63%]
test_kpop_concert.py::test_validasi_penonton_kategori_tidak_dikenal_raises PASSED [ 68%]
test_kpop_concert.py::test_validasi_penonton_festival_dewasa_lolos PASSED [ 72%]
test_kpop_concert.py::test_validasi_penonton_festival_remaja_dengan_surat_izin_lolos PASSED [ 77%]
test_kpop_concert.py::test_validasi_penonton_seated_anak_lolos PASSED    [ 81%]
test_kpop_concert.py::test_proses_booking_sukses_dengan_mock PASSED      [ 86%]
test_kpop_concert.py::test_proses_booking_notifikasi_gagal_dengan_mock PASSED [ 90%]
test_kpop_concert.py::test_proses_booking_gateway_timeout_dengan_mock PASSED [ 95%]
test_kpop_concert.py::test_proses_booking_data_kosong_raises PASSED      [100%]

=============================== tests coverage ================================
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
kpop_concert.py      51      0     30      0   100%
-------------------------------------------------------------
TOTAL                51      0     30      0   100%
============================= 22 passed in 0.49s ==============================
```

### Analisis Branch Coverage:
- **Total Statement**: 51 baris dieksekusi 100% (Miss: 0).
- **Total Cabang Keputusan (Branch)**: 30 percabangan kondisi logika (`if`, `elif`, `else`, `try-except`).
- **Partial Branch (BrPart)**: 0, artinya tidak ada satu pun cabang yang hanya diuji sebagian. Seluruh jalur kondisi bernilai `True` maupun `False` telah diuji secara lengkap.
- Laporan HTML interaktif juga tersedia di folder `htmlcov/index.html`.
