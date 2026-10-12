def cariTransaksi(transaksi, idTransaksi):
    for t in transaksi:
        if t["id"] == idTransaksi:
            return t

    return None

def buatTransaksi(transaksi, tipe, nominal, tanggal, kategori, deskripsi):
    idTerbesar = 0

    for t in transaksi:
        if t["id"] > idTerbesar:
            idTerbesar = t["id"]

    idBaru = idTerbesar + 1

    # Membuat data transaksi
    dataTransaksi = {
        "id": idBaru,
        "tanggal": tanggal,
        "tipe": tipe,
        "nominal": nominal,
        "kategori": kategori,
        "deskripsi": deskripsi
    }

    # Menambahkan transaksi ke daftar
    transaksi.append(dataTransaksi)

    return dataTransaksi