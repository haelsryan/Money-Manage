transaksi = []

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

def tambahTransaksi():
    print("\n=== Tambah Transaksi ===")
    tipeTransaksi = input("Masukkan tipe transaksi (pemasukan/pengeluaran): ").lower()
    if tipeTransaksi != 'pemasukan' and tipeTransaksi != 'pengeluaran':
        print("Tipe transaksi tidak valid. Harap masukkan 'pemasukan' atau 'pengeluaran'.")
        return
    nominal = int(input("Nominal : "))
    kategori = input("Kategori : ")
    deskripsi = input("Deskripsi : ")
    dataTransaksi = {
        "id": len(transaksi) + 1,
        "tipe": tipeTransaksi,
        "nominal": nominal,
        "kategori": kategori,
        "deskripsi": deskripsi
    }
    transaksi.append(dataTransaksi)
    print("Transaksi berhasil ditambahkan!")

def lihatTransaksi():
    print("\n=== Daftar Transaksi ===")
    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        return

    for t in transaksi:
        print("------------")
        print(f"ID      : {t['id']}")
        print(f"Tipe    : {t['tipe']}")
        print(f"Nominal : Rp.{t['nominal']}")
        print(f"Kategori: {t['kategori']}")
        print(f"Deskripsi: {t['deskripsi']}")

def editTransaksi():
    print("\n=== Cari Transaksi ===")
    idTransaksi = int(input("Masukkan ID transaksi : "))
    for t in transaksi:
        if t["id"] == idTransaksi:
            print("\nTransaksi ditemukan:")
            print("------------")
            print(f"Nominal Sebelum : Rp.{t['nominal']}")
            nominalBaru = int(input("Masukkan nominal baru : "))
            t["nominal"] = nominalBaru
            tipeBaru = input("Masukkan tipe transaksi baru (pemasukan/pengeluaran) : ").lower()
            if tipeBaru != 'pemasukan' and tipeBaru != 'pengeluaran':
                print("Tipe transaksi tidak valid. Harap masukkan 'pemasukan' atau 'pengeluaran'.")
                return
            t["tipe"] = tipeBaru
            kategoriBaru = input("Masukkan kategori baru : ")
            t["kategori"] = kategoriBaru
            deskripsiBaru = input("Masukkan deskripsi baru : ")
            t["deskripsi"] = deskripsiBaru
            print("Transaksi berhasil diubah!")
            return
    print("Transaksi dengan ID tersebut tidak ditemukan.")

def hapusTransaksi():
    print("\n=== Hapus Transaksi ===")
    idTransaksi = int(input("Masukkan ID transaksi yang ingin dihapus: "))
    for t in transaksi:
        if t["id"] == idTransaksi:
            transaksi.remove(t)
            print("Transaksi berhasil dihapus!")
            return
    print("Transaksi dengan ID tersebut tidak ditemukan.")

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
    print(f"Total Pemasukan   : Rp.{totalPemasukan}")
    print(f"Total Pengeluaran : Rp.{totalPengeluaran}")
    print(f"Saldo Bersih      : Rp.{saldo}")

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
