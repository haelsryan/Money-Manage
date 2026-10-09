def hitungSaldo(transaksi):
    totalPemasukan = 0
    totalPengeluaran = 0

    for t in transaksi:
        if t["tipe"] == "pemasukan":
            totalPemasukan += t["nominal"]
        elif t["tipe"] == "pengeluaran":
            totalPengeluaran += t["nominal"]

    saldo = totalPemasukan - totalPengeluaran
    return totalPemasukan, totalPengeluaran, saldo

def laporanKeuangan(transaksi):
    totalPemasukan = 0
    totalPengeluaran = 0
    jumlahPemasukan = 0
    jumlahPengeluaran = 0
    pengeluaranKategori = {}
    pemasukanKategori = {}
    
    for t in transaksi:
        if t["tipe"] == "pemasukan":
            totalPemasukan += t["nominal"]
            jumlahPemasukan += 1
            kategori = t["kategori"]
            if kategori not in pemasukanKategori:
                pemasukanKategori[kategori] = 0
            pemasukanKategori[kategori] += t["nominal"]
    
        if t["tipe"] == "pengeluaran":
            totalPengeluaran += t["nominal"]
            jumlahPengeluaran += 1
            kategori = t["kategori"]
            if kategori not in pengeluaranKategori:
                pengeluaranKategori[kategori] = 0
            pengeluaranKategori[kategori] += t["nominal"]

    saldo = totalPemasukan - totalPengeluaran
    transaksiTerbesar = max(transaksi, key=lambda t: t["nominal"])

    return {
        "jumlahTransaksi": len(transaksi),
        "jumlahPemasukan": jumlahPemasukan,
        "jumlahPengeluaran": jumlahPengeluaran,
        "totalPemasukan": totalPemasukan,
        "totalPengeluaran": totalPengeluaran,
        "saldo": saldo,
        "pemasukanKategori": pemasukanKategori,
        "pengeluaranKategori": pengeluaranKategori,
        "transaksiTerbesar": transaksiTerbesar
    }