"""
Modul layanan eksternal untuk pengiriman E-Ticket konser K-Pop.
Modul ini bertindak sebagai dependensi eksternal (third-party gateway)
yang akan di-mock dalam pengujian unit test.
"""

def kirim_notifikasi_eticket(email: str, booking_id: str, detail_pesanan: dict) -> bool:
    """
    Simulasi pengiriman email / notifikasi E-Ticket ke pembeli.
    Pada kondisi nyata, fungsi ini memanggil API gateway email/SMS/WhatsApp.
    """
    print(f"[LIVE GATEWAY] Mengirim E-Ticket {booking_id} ke {email}...")
    # Dalam kondisi nyata ini terhubung ke jaringan/API eksternal
    return True
