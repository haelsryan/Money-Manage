import json
import os
from datetime import datetime
transaksi = []
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def formatRupiah(nominal):
    return f"Rp.{nominal:,}".replace(",", ".")

def tampilkanDetail(t):
    print("------------")
    print(f"ID        : {t['id']}")
    print(f"Tanggal   : {t['tanggal']}")
    print(f"Tipe      : {t['tipe']}")
    print(f"Nominal   : {formatRupiah(t['nominal'])}")
    print(f"Kategori  : {t['kategori']}")
    print(f"Deskripsi : {t['deskripsi']}")
    print("------------")

def cariTransaksi(idTransaksi):
    for t in transaksi:
        if t["id"] == idTransaksi:
            return t
        
    return None

def pilihKategori():
    print("\n=== Pilih Kategori ===")
    print("1. Makanan & Minuman")
    print("2. Transportasi")
    print("3. Belanja")
    print("4. Hiburan")
    print("5. Pendidikan")
    print("6. Lainnya")
    print("----------------")
    pilihan = input("Masukkan nomor kategori: ")

    kategori = {
        "1": "Makanan & Minuman",
        "2": "Transportasi",
        "3": "Belanja",
        "4": "Hiburan",
        "5": "Pendidikan",
        "6": "Lainnya"
    }

    if pilihan in kategori:
        return kategori[pilihan]

    print("Pilihan kategori tidak valid. Silakan coba lagi.")
    return None

def showMenu():
    print("\n================")
    print("  Money Manager ")
    print("================")
    print("1. Tambah Transaksi")
    print("2. Lihat Transaksi")
    print("3. Edit Transaksi")
    print("4. Hapus Transaksi")
    print("5. Lihat Saldo")
    print("0. Keluar")
    print("----------------")

def tambahTransaksi():
    print("\n=== Tambah Transaksi ===")
    tipeTransaksi = input("Masukkan tipe transaksi (pemasukan/pengeluaran): ").lower()
    if tipeTransaksi != 'pemasukan' and tipeTransaksi != 'pengeluaran':
        print("Tipe transaksi tidak valid. Harap masukkan 'pemasukan' atau 'pengeluaran'.")
        return

    # ID Baru
    idTerbesar = 0
    for t in transaksi:
        if t["id"] > idTerbesar:
            idTerbesar = t["id"]
    idBaru = idTerbesar + 1

    # Input Nominal
    try:
        nominal = int(input("Nominal : "))
    except ValueError:
        print("Nominal harus berupa angka.")
        return

    if nominal <= 0:
        print("Nominal harus lebih besar dari 0.")
        return
    # Tanggal Transaksi
    tanggal = datetime.now().strftime("%d - %m - %Y")

    # Pilih Kategori
    kategori = pilihKategori()
    if kategori is None:
        return

    # Input Deskripsi
    deskripsi = input("Deskripsi : ")

    # Membuat data transaksi baru
    dataTransaksi = {
        "id": idBaru,
        "tanggal": tanggal,
        "tipe": tipeTransaksi,
        "nominal": nominal,
        "kategori": kategori,
        "deskripsi": deskripsi
    }
    transaksi.append(dataTransaksi)
    saveData()

    print("\nTransaksi berhasil ditambahkan!")
    print(f"ID Transaksi : {idBaru}")
    print(f"Tanggal      : {tanggal}")
    print(f"Tipe         : {tipeTransaksi}")
    print(f"Nominal      : {formatRupiah(nominal)}")
    print(f"Kategori     : {kategori}")
    print(f"Deskripsi    : {deskripsi}")

def lihatTransaksi():
    print("\n=== Daftar Transaksi ===")

    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        return

    for t in transaksi:
        tampilkanDetail(t)

def editTransaksi():
    print("\n=== Cari Transaksi ===")

    # Mencari transaksi berdasarkan ID
    try:
        idTransaksi = int(input("Masukkan ID transaksi : "))
    except ValueError:
        print("ID transaksi harus berupa angka.")
        return

    t = cariTransaksi(idTransaksi)

    if t is None:
            print("Transaksi ID tidak ditemukan.")
            return

    print("\n- Transaksi Ditemukan : ")
    tampilkanDetail(t)

    try:
        nominalBaru = int(input("Masukkan nominal baru : "))
    except ValueError:
        print("Nominal harus berupa angka.")
        return

    tipeBaru = input("Masukkan tipe transaksi baru (pemasukan/pengeluaran) : ").lower()
    if tipeBaru != "pemasukan" and tipeBaru != "pengeluaran":
        print("Tipe transaksi tidak valid.")
        return

    kategoriBaru = pilihKategori()

    if kategoriBaru is None:
        return

    deskripsiBaru = input("Masukkan deskripsi baru : ")

    t["nominal"] = nominalBaru
    t["tipe"] = tipeBaru
    t["kategori"] = kategoriBaru
    t["deskripsi"] = deskripsiBaru
    saveData()
    print("\nTransaksi berhasil diubah!")

def hapusTransaksi():
    print("\n=== Hapus Transaksi ===")

    try:
        idTransaksi = int(input("Masukkan ID transaksi yang ingin dihapus: "))
    except ValueError:
        print("ID transaksi harus berupa angka.")
        return
    
    t = cariTransaksi(idTransaksi)
    if t is None:
        print("Transaksi ID tidak ditemukan.")
        return
    
    print("\n- Transaksi Yang Akan Dihapus :")
    tampilkanDetail(t)
    konfirmasi = input("Apakah anda yakin untuk menghapus transaksi ini? (y/n) : ").lower()

    if konfirmasi == "y":
        transaksi.remove(t)
        saveData()
        print("Transaksi berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")
    return

def lihatSaldo():
    totalPemasukan = 0
    totalPengeluaran = 0
    for t in transaksi:
        if t["tipe"] == "pemasukan":
            totalPemasukan += t["nominal"]
        elif t["tipe"] == "pengeluaran":
            totalPengeluaran += t["nominal"]
    saldo = totalPemasukan - totalPengeluaran
    print("\n=== Saldo Saat Ini ===")
    print(f"Total Pemasukan   : {formatRupiah(totalPemasukan)}")
    print(f"Total Pengeluaran : {formatRupiah(totalPengeluaran)}")
    print(f"Saldo Bersih      : {formatRupiah(saldo)}")

def saveData():
    with open(DATA_FILE, "w") as file:
        json.dump(transaksi, file, indent=4)

def loadData():
    global transaksi
    try:
        with open(DATA_FILE, "r") as file:
            transaksi = json.load(file)
    except FileNotFoundError:
        transaksi = []
    except json.JSONDecodeError:
        print("Data JSON rusak atau tidak valid.")
        transaksi = []

loadData()
while True:
    showMenu()
    choice = input("Pilih menu: ")

    if choice == "1":
        tambahTransaksi()
    elif choice == "2":
        lihatTransaksi()
    elif choice == "3":
        editTransaksi()
    elif choice == "4":
        hapusTransaksi()
    elif choice == "5":
        lihatSaldo()
    elif choice == "0":
        print("\nTerima kasih telah menggunakan Money Manager!")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")