"""
Script Demo Pengujian Manual (demo_manual.py)
Jalankan file ini dengan perintah: python demo_manual.py

Script ini mendemonstrasikan secara langsung cara kerja 4 kriteria tugas Sesi 9:
1. Pengujian Nilai Batas (BVA) & Perhitungan Diskon
2. Pengujian Skenario Negatif (Exception ValueError & PermissionError)
3. Pengujian Fixture Setup & Cleanup (Pola Yield)
4. Pengujian Mocking Layanan Eksternal (unittest.mock.patch)
"""

from unittest.mock import patch
from kpop_concert import hitung_harga_tiket, validasi_penonton, proses_booking_tiket


def pemisah(judul):
    print("\n" + "=" * 65)
    print(f" {judul}")
    print("=" * 65)


def demo_bva_diskon():
    pemisah("1. DEMO PENGUJIAN MANUAL BVA (BOUNDARY VALUE ANALYSIS)")
    print("Kategori: VIP_SOUNDCHECK (Harga dasar: Rp 3.500.000)")
    print("Range valid pembelian: 1 s.d. 4 tiket per akun\n")
    
    skenario_bva = [
        (1, True, "Batas Bawah Valid (1 tiket) -> Diskon Member 5%"),
        (2, True, "Titik Sebelum Naik Tier (2 tiket) -> Diskon Member 5%"),
        (3, True, "Titik Awal Tier Besar (3 tiket) -> Diskon Member 10%"),
        (4, True, "Batas Atas Kuota War (4 tiket) -> Diskon Member 10%"),
    ]
    
    for jumlah, member, ket in skenario_bva:
        total = hitung_harga_tiket("VIP_SOUNDCHECK", jumlah, membership=member)
        print(f"[*] Input: {jumlah} tiket | Member: {member}")
        print(f"    Keterangan : {ket}")
        print(f"    Hasil Bayar: Rp {total:,}\n")


def demo_skenario_negatif():
    pemisah("2. DEMO PENGUJIAN SKENARIO NEGATIF (EXCEPTION / RAISES)")
    
    # Kasus 1: Beli 5 tiket (melebihi batas maksimal 4)
    print("[*] Kasus Negatif 1: Mencoba beli 5 tiket (melebihi kuota war)")
    try:
        hitung_harga_tiket("VIP_SOUNDCHECK", jumlah_tiket=5)
    except ValueError as e:
        print(f"    -> BERHASIL DITANGKAP: [ValueError] {e}\n")
        
    # Kasus 2: Penonton 14 tahun di Festival tanpa surat izin orang tua
    print("[*] Kasus Negatif 2: Penonton 14 tahun masuk area Festival tanpa izin wali")
    try:
        validasi_penonton(usia=14, kategori="CAT_1_FESTIVAL", surat_izin=False)
    except PermissionError as e:
        print(f"    -> BERHASIL DITANGKAP: [PermissionError] {e}\n")


def demo_fixture_cleanup():
    pemisah("3. DEMO PENGUJIAN MANUAL FIXTURE & CLEANUP (YIELD)")
    print("Simulasi alur @pytest.fixture dengan cleanup (yield):")
    
    # SETUP
    print("1. [SETUP] Inisialisasi antrean booking di memori...")
    data_booking = {"booking_id": "KPOP-DEMO-01", "nama": "Azzahra", "kategori": "VIP_SOUNDCHECK"}
    print(f"   State awal: {data_booking}")
    
    # TEST / EKSEKUSI
    print("2. [TEST RUN] Fungsi pengujian membaca data dari fixture:")
    assert data_booking["booking_id"] == "KPOP-DEMO-01"
    print(f"   Assertion lolos: ID Booking '{data_booking['booking_id']}' cocok.")
    
    # CLEANUP
    print("3. [CLEANUP] Menjalankan kode setelah 'yield' untuk teardown:")
    data_booking.clear()
    print(f"   State akhir setelah cleanup: {data_booking} (bersih kembali)\n")


def demo_mocking():
    pemisah("4. DEMO PENGUJIAN MANUAL MOCKING (ISOLASI DEPENDENSI)")
    print("Kita memanggil proses_booking_tiket() tanpa koneksi email asli.")
    
    # Menggunakan patch untuk mengganti fungsi kirim_notifikasi_eticket dengan Mock
    with patch("kpop_concert.kirim_notifikasi_eticket", return_value=True) as mock_service:
        hasil = proses_booking_tiket(
            booking_id="KPOP-NCT-777",
            nama_pemesan="Azzahra Fan",
            email="azzahra@kpopmail.com",
            usia=20,
            kategori="VIP_SOUNDCHECK",
            jumlah_tiket=2,
            membership=True
        )
        print("[*] Hasil Kembalian Fungsi:")
        print(f"    Status     : {hasil['status']}")
        print(f"    Booking ID : {hasil['booking_id']}")
        print(f"    Total Bayar: Rp {hasil['total_bayar']:,}")
        print(f"    Pesan      : {hasil['pesan']}")
        
        # Verifikasi interaksi mock
        print("\n[*] Verifikasi Mock:")
        print(f"    Apakah fungsi email eksternal dipanggil? {mock_service.called}")
        print(f"    Berapa kali dipanggil? {mock_service.call_count} kali")
        print(f"    Argumen pemanggilan: {mock_service.call_args[0][:2]}")
        print("    -> Hasil: Berhasil diisolasi 100% tanpa internet/gateway nyata!\n")


if __name__ == "__main__":
    demo_bva_diskon()
    demo_skenario_negatif()
    demo_fixture_cleanup()
    demo_mocking()
    print("=" * 65)
    print(" SEMUA PENGUJIAN MANUAL BERHASIL DIJALANKAN DENGAN BENAR!")
    print("=" * 65)
