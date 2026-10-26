"""
File Test PyTest untuk Modul Pemesanan Tiket Konser K-Pop (test_kpop_concert.py).

Mencakup:
(1) Minimal 8 test, termasuk 1 `@pytest.mark.parametrize` berbasis BVA (Boundary Value Analysis).
(2) Minimal 2 test `pytest.raises` untuk skenario negatif.
(3) Minimal 1 `fixture` (dengan cleanup memakai `yield`).
(4) Penggunaan `mock` (`unittest.mock.patch`) untuk isolasi dependensi eksternal.
"""

from unittest.mock import patch
import pytest

from kpop_concert import (
    HARGA_TIKET,
    hitung_harga_tiket,
    validasi_penonton,
    proses_booking_tiket
)


# ==============================================================================
# BAGIAN 1: FIXTURE DENGAN CLEANUP MEMAKAI `yield`
# ==============================================================================
@pytest.fixture
def antrean_booking_session():
    """
    Fixture untuk mengelola state data pemesanan sementara (in-memory hold).
    Menggunakan pola:
    - Setup (Arrange): Inisialisasi data pemesanan sebelum test berjalan.
    - yield: Memberikan state pemesanan ke fungsi test.
    - Cleanup (Teardown): Membersihkan data antrean setelah test selesai.
    """
    # 1. SETUP
    data_booking = {
        "booking_id": "KPOP-NCT-777",
        "nama_pemesan": "Azzahra Fan",
        "email": "azzahra@kpopmail.com",
        "usia": 20,
        "kategori": "VIP_SOUNDCHECK",
        "jumlah_tiket": 2,
        "membership": True,
        "surat_izin": False
    }
    
    # 2. YIELD (Diserahkan ke fungsi pengujian)
    yield data_booking
    
    # 3. CLEANUP (Dijalankan otomatis setelah test selesai)
    data_booking.clear()


def test_fixture_setup_dan_cleanup(antrean_booking_session):
    """
    Memverifikasi bahwa fixture berhasil menyediakan data awal yang valid.
    """
    assert antrean_booking_session["booking_id"] == "KPOP-NCT-777"
    assert antrean_booking_session["kategori"] == "VIP_SOUNDCHECK"
    assert antrean_booking_session["jumlah_tiket"] == 2


# ==============================================================================
# BAGIAN 2: PARAMETRIZE BERBASIS BVA (Boundary Value Analysis)
# ==============================================================================
@pytest.mark.parametrize("jumlah_tiket, diskon_diharapkan, keterangan", [
    (1, 0.05, "Batas bawah valid (1 tiket) -> Diskon Member 5%"),
    (2, 0.05, "Titik batas sebelum naik tier (2 tiket) -> Diskon Member 5%"),
    (3, 0.10, "Titik batas awal tier diskon besar (3 tiket) -> Diskon Member 10%"),
    (4, 0.10, "Batas atas valid kuota war tiket (4 tiket) -> Diskon Member 10%"),
])
def test_bva_hitung_harga_tiket_member(jumlah_tiket, diskon_diharapkan, keterangan):
    """
    Pengujian BVA (Boundary Value Analysis) untuk jumlah_tiket [1, 4] bagi pembeli Fanclub Member.
    Kategori yang diuji: VIP_SOUNDCHECK (Rp 3.500.000).
    """
    harga_satuan = HARGA_TIKET["VIP_SOUNDCHECK"]
    subtotal = harga_satuan * jumlah_tiket
    total_ekspektasi = int(subtotal * (1 - diskon_diharapkan))
    
    total_hasil = hitung_harga_tiket(
        kategori="VIP_SOUNDCHECK",
        jumlah_tiket=jumlah_tiket,
        membership=True
    )
    assert total_hasil == total_ekspektasi, f"Gagal pada kasus: {keterangan}"


def test_hitung_harga_non_member_tanpa_diskon():
    """Menguji non-member yang membeli di bawah 4 tiket (tidak mendapat diskon)."""
    # 2 tiket CAT 1 @ 2.500.000 = 5.000.000
    total = hitung_harga_tiket("CAT_1_FESTIVAL", jumlah_tiket=2, membership=False)
    assert total == 5_000_000


def test_hitung_harga_non_member_bundle_diskon():
    """Menguji non-member yang membeli tepat di batas atas 4 tiket (diskon bundle 2%)."""
    # 4 tiket CAT 2 @ 1.500.000 = 6.000.000 - 2% (120.000) = 5.880.000
    total = hitung_harga_tiket("CAT_2_SEATED", jumlah_tiket=4, membership=False)
    assert total == 5_880_000


# ==============================================================================
# BAGIAN 3: PENGUJIAN SKENARIO NEGATIF DENGAN pytest.raises (Minimal 2 Test)
# ==============================================================================
def test_hitung_harga_tiket_jumlah_kurang_dari_satu_raises():
    """Skenario Negatif 1: Jumlah tiket 0 (di bawah batas minimum) melempar ValueError."""
    with pytest.raises(ValueError, match="Jumlah tiket minimal adalah 1"):
        hitung_harga_tiket("VIP_SOUNDCHECK", jumlah_tiket=0, membership=True)


def test_hitung_harga_tiket_melebihi_kuota_war_raises():
    """Skenario Negatif 2: Jumlah tiket 5 (melebihi batas maksimal 4) melempar ValueError."""
    with pytest.raises(ValueError, match="Maksimal pembelian adalah 4 tiket"):
        hitung_harga_tiket("CAT_1_FESTIVAL", jumlah_tiket=5, membership=False)


def test_hitung_harga_kategori_tidak_valid_raises():
    """Skenario Negatif 3: Kategori tidak ada dalam daftar tiket melempar ValueError."""
    with pytest.raises(ValueError, match="tidak valid"):
        hitung_harga_tiket("CAT_VVIP_LUXURY", jumlah_tiket=1)


def test_validasi_penonton_standing_di_bawah_12_tahun_raises():
    """Skenario Negatif 4: Anak di bawah 12 tahun dilarang di area standing festival."""
    with pytest.raises(PermissionError, match="dilarang di area standing"):
        validasi_penonton(usia=11, kategori="VIP_SOUNDCHECK", surat_izin=True)


def test_validasi_penonton_remaja_tanpa_surat_izin_raises():
    """Skenario Negatif 5: Penonton 14 tahun di area standing tanpa surat izin wali."""
    with pytest.raises(PermissionError, match="wajib melampirkan surat izin wali"):
        validasi_penonton(usia=14, kategori="CAT_1_FESTIVAL", surat_izin=False)


def test_validasi_penonton_balita_di_venue_raises():
    """Skenario Negatif 6: Anak di bawah 7 tahun dilarang di area seated."""
    with pytest.raises(PermissionError, match="Anak di bawah 7 tahun tidak diperkenankan"):
        validasi_penonton(usia=5, kategori="CAT_2_SEATED")


def test_validasi_penonton_usia_tidak_wajar_raises():
    """Skenario Negatif 7: Usia negatif atau di atas 100 melempar ValueError."""
    with pytest.raises(ValueError, match="Usia tidak valid"):
        validasi_penonton(usia=-1, kategori="CAT_2_SEATED")
    with pytest.raises(ValueError, match="Usia tidak valid"):
        validasi_penonton(usia=105, kategori="CAT_2_SEATED")


def test_validasi_penonton_kategori_tidak_dikenal_raises():
    """Skenario Negatif 8: Kategori tidak dikenal saat validasi melempar ValueError."""
    with pytest.raises(ValueError, match="tidak dikenali"):
        validasi_penonton(usia=20, kategori="CAT_UNKNOWN")


# ==============================================================================
# BAGIAN 4: PENGUJIAN SKENARIO POSITIF VALIDASI
# ==============================================================================
def test_validasi_penonton_festival_dewasa_lolos():
    """Penonton dewasa (>=17 tahun) lolos masuk area festival tanpa syarat surat izin."""
    assert validasi_penonton(usia=17, kategori="VIP_SOUNDCHECK", surat_izin=False) is True


def test_validasi_penonton_festival_remaja_dengan_surat_izin_lolos():
    """Penonton remaja (12-16 tahun) lolos jika melampirkan surat izin orang tua/wali."""
    assert validasi_penonton(usia=15, kategori="CAT_1_FESTIVAL", surat_izin=True) is True


def test_validasi_penonton_seated_anak_lolos():
    """Anak usia 8 tahun lolos masuk kategori seated (CAT 2)."""
    assert validasi_penonton(usia=8, kategori="CAT_2_SEATED") is True


# ==============================================================================
# BAGIAN 5: PENGUJIAN MOCKING DENGAN unittest.mock.patch
# ==============================================================================
def test_proses_booking_sukses_dengan_mock(antrean_booking_session):
    """
    Menguji proses booking berhasil dan memverifikasi notifikasi E-Ticket terkirim
    menggunakan Mock untuk mengisolasi gateway email eksternal.
    """
    with patch("kpop_concert.kirim_notifikasi_eticket", return_value=True) as mock_eticket:
        hasil = proses_booking_tiket(
            booking_id=antrean_booking_session["booking_id"],
            nama_pemesan=antrean_booking_session["nama_pemesan"],
            email=antrean_booking_session["email"],
            usia=antrean_booking_session["usia"],
            kategori=antrean_booking_session["kategori"],
            jumlah_tiket=antrean_booking_session["jumlah_tiket"],
            membership=antrean_booking_session["membership"]
        )
        
        # Assertion hasil proses
        assert hasil["status"] == "CONFIRMED"
        assert hasil["booking_id"] == "KPOP-NCT-777"
        assert "E-Ticket berhasil diterbitkan" in hasil["pesan"]
        
        # Verifikasi mock dipanggil tepat 1 kali dengan argumen yang benar
        mock_eticket.assert_called_once()
        args, _ = mock_eticket.call_args
        assert args[0] == "azzahra@kpopmail.com"
        assert args[1] == "KPOP-NCT-777"


def test_proses_booking_notifikasi_gagal_dengan_mock(antrean_booking_session):
    """
    Menguji kondisi saat pembayaran berhasil tetapi gateway notifikasi mengembalikan False.
    """
    with patch("kpop_concert.kirim_notifikasi_eticket", return_value=False) as mock_eticket:
        hasil = proses_booking_tiket(
            booking_id=antrean_booking_session["booking_id"],
            nama_pemesan=antrean_booking_session["nama_pemesan"],
            email=antrean_booking_session["email"],
            usia=antrean_booking_session["usia"],
            kategori=antrean_booking_session["kategori"],
            jumlah_tiket=antrean_booking_session["jumlah_tiket"],
            membership=antrean_booking_session["membership"]
        )
        assert hasil["status"] == "PENDING_NOTIFIKASI"
        assert "pengiriman E-Ticket tertunda" in hasil["pesan"]
        mock_eticket.assert_called_once()


def test_proses_booking_gateway_timeout_dengan_mock(antrean_booking_session):
    """
    Menguji penanganan error ketika gateway eksternal mengalami gangguan/timeout (side_effect).
    """
    with patch("kpop_concert.kirim_notifikasi_eticket", side_effect=ConnectionError("Gateway Timeout")):
        hasil = proses_booking_tiket(
            booking_id=antrean_booking_session["booking_id"],
            nama_pemesan=antrean_booking_session["nama_pemesan"],
            email=antrean_booking_session["email"],
            usia=antrean_booking_session["usia"],
            kategori=antrean_booking_session["kategori"],
            jumlah_tiket=antrean_booking_session["jumlah_tiket"],
            membership=antrean_booking_session["membership"]
        )
        assert hasil["status"] == "GATEWAY_ERROR"
        assert "Gagal terhubung ke layanan E-Ticket" in hasil["pesan"]


def test_proses_booking_data_kosong_raises():
    """Menguji skenario negatif ketika data identitas pemesan kosong."""
    with pytest.raises(ValueError, match="Data pemesan .* tidak boleh kosong"):
        proses_booking_tiket(
            booking_id="",
            nama_pemesan="Azzahra",
            email="az@test.com",
            usia=20,
            kategori="VIP_SOUNDCHECK",
            jumlah_tiket=1
        )
