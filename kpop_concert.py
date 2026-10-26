"""
Modul Sistem Pemesanan Tiket Konser K-Pop ("K-Pop World Tour Fest").
Berisi 3 fungsi berlogika bersyarat:
1. hitung_harga_tiket: Menghitung total harga tiket dengan diskon bertingkat (BVA).
2. validasi_penonton: Memvalidasi kriteria batas usia penonton & regulasi area konser.
3. proses_booking_tiket: Memproses transaksi tiket & integrasi layanan notifikasi (Mocking).
"""

from ticket_service import kirim_notifikasi_eticket

# Daftar harga resmi kategori tiket konser K-Pop
HARGA_TIKET = {
    "VIP_SOUNDCHECK": 3_500_000,   # Termasuk soundcheck pass & lanyards
    "CAT_1_FESTIVAL": 2_500_000,   # Area berdiri (standing pit) dekat panggung
    "CAT_2_SEATED": 1_500_000      # Area duduk bernomor
}

# Batasan pembelian war tiket resmi
MIN_TIKET = 1
MAX_TIKET = 4


def hitung_harga_tiket(kategori: str, jumlah_tiket: int, membership: bool = False) -> int:
    """
    Menghitung total pembayaran tiket konser K-Pop berdasarkan kategori dan membership.
    
    Aturan:
    - Kategori harus terdaftar di HARGA_TIKET.
    - Jumlah tiket per akun: 1 sampai 4 tiket (aturan war tiket konser).
    - Jika pembeli memiliki Global Fanclub Membership (membership=True):
        * Pembelian 3 s.d. 4 tiket: Diskon 10% (0.10)
        * Pembelian 1 s.d. 2 tiket: Diskon 5% (0.05)
    - Jika non-membership (membership=False):
        * Pembelian 4 tiket (paket rombongan): Diskon 2% (0.02)
        * Pembelian 1 s.d. 3 tiket: Diskon 0% (tidak ada diskon)
    """
    if kategori not in HARGA_TIKET:
        raise ValueError(f"Kategori tiket '{kategori}' tidak valid. Pilih: {list(HARGA_TIKET.keys())}")
    
    if jumlah_tiket < MIN_TIKET:
        raise ValueError(f"Jumlah tiket minimal adalah {MIN_TIKET}.")
    
    if jumlah_tiket > MAX_TIKET:
        raise ValueError(f"Maksimal pembelian adalah {MAX_TIKET} tiket per akun.")
    
    harga_satuan = HARGA_TIKET[kategori]
    subtotal = harga_satuan * jumlah_tiket
    
    if membership:
        if jumlah_tiket >= 3:
            diskon = 0.10
        else:
            diskon = 0.05
    else:
        if jumlah_tiket == 4:
            diskon = 0.02
        else:
            diskon = 0.0
            
    total_bayar = int(subtotal * (1 - diskon))
    return total_bayar


def validasi_penonton(usia: int, kategori: str, surat_izin: bool = False) -> bool:
    """
    Validasi kelayakan penonton konser K-Pop berdasarkan usia dan kategori tiket.
    
    Regulasi Keamanan Venue:
    - Usia tidak boleh kurang dari 0 atau lebih dari 100 tahun.
    - Kategori Festival/Standing ('VIP_SOUNDCHECK' & 'CAT_1_FESTIVAL'):
        * Usia < 12 tahun dilarang di area standing festival demi keselamatan crowd.
        * Usia 12 - 16 tahun (usia < 17) wajib memiliki surat izin wali/orang tua.
        * Usia >= 17 tahun lolos tanpa syarat surat izin.
    - Kategori Duduk ('CAT_2_SEATED'):
        * Usia < 7 tahun dilarang memasuki venue.
        * Usia >= 7 tahun diperbolehkan.
    """
    if usia < 0 or usia > 100:
        raise ValueError("Usia tidak valid.")
    
    if kategori in ("VIP_SOUNDCHECK", "CAT_1_FESTIVAL"):
        if usia < 12:
            raise PermissionError("Anak di bawah 12 tahun dilarang di area standing demi keselamatan.")
        if usia < 17:
            if not surat_izin:
                raise PermissionError("Penonton berusia 12-16 tahun wajib melampirkan surat izin wali di area standing.")
            return True
        return True
    
    if kategori == "CAT_2_SEATED":
        if usia < 7:
            raise PermissionError("Anak di bawah 7 tahun tidak diperkenankan memasuki venue konser.")
        return True
        
    raise ValueError(f"Kategori '{kategori}' tidak dikenali untuk validasi venue.")


def proses_booking_tiket(
    booking_id: str,
    nama_pemesan: str,
    email: str,
    usia: int,
    kategori: str,
    jumlah_tiket: int,
    membership: bool = False,
    surat_izin: bool = False
) -> dict:
    """
    Memproses pemesanan tiket konser, memvalidasi penonton, menghitung harga,
    dan mengirim E-Ticket melalui layanan notifikasi eksternal.
    """
    if not booking_id or not nama_pemesan or not email:
        raise ValueError("Data pemesan (booking_id, nama, email) tidak boleh kosong.")
    
    # 1. Validasi penonton
    validasi_penonton(usia=usia, kategori=kategori, surat_izin=surat_izin)
    
    # 2. Hitung harga tiket
    total_bayar = hitung_harga_tiket(kategori=kategori, jumlah_tiket=jumlah_tiket, membership=membership)
    
    detail_pesanan = {
        "booking_id": booking_id,
        "nama": nama_pemesan,
        "email": email,
        "kategori": kategori,
        "jumlah": jumlah_tiket,
        "total_bayar": total_bayar
    }
    
    # 3. Panggil layanan notifikasi eksternal (akan diuji dengan mock)
    try:
        notif_berhasil = kirim_notifikasi_eticket(email, booking_id, detail_pesanan)
    except Exception as e:
        return {
            "status": "GATEWAY_ERROR",
            "booking_id": booking_id,
            "total_bayar": total_bayar,
            "pesan": f"Gagal terhubung ke layanan E-Ticket: {str(e)}"
        }
        
    if notif_berhasil:
        return {
            "status": "CONFIRMED",
            "booking_id": booking_id,
            "total_bayar": total_bayar,
            "pesan": "E-Ticket berhasil diterbitkan dan dikirim ke email."
        }
    else:
        return {
            "status": "PENDING_NOTIFIKASI",
            "booking_id": booking_id,
            "total_bayar": total_bayar,
            "pesan": "Pembayaran sukses namun pengiriman E-Ticket tertunda."
        }
