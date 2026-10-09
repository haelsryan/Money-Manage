# IMPORT PACKAGE YANG DIBUTUHKAN
from datetime import datetime
import validasi
import storage
import keuangan
transaksi = storage.loadData()

# FORMAT RUPIAH (Rp. x.xxx.xxx)
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
            
def searchTransaksi():
    print("\n=== Cari Transaksi ===")
    keyword = input("Masukkan kata kunci : ").strip().lower()

    if not keyword:
        print("Kata kunci tidak boleh kosong")
        return

    ditemukan = False
    for t in transaksi:
        if keyword in t["deskripsi"].lower():
            tampilkanDetail(t)
            ditemukan = True
        if not ditemukan:
            print("Transaksi tidak ditemukan")

def pilihKategori():
    kategori = {
        "1": "Makanan & Minuman",
        "2": "Transportasi",
        "3": "Belanja",
        "4": "Hiburan",
        "5": "Pendidikan",
        "6": "Lainnya"
    }

    while True:    
        print("\n=== Pilih Kategori ===")
        for nomor, nama in kategori.items():
            print(f"{nomor}. {nama}")
        print("----------------")
        pilihan = input("Masukkan nomor kategori: ").strip()

        if pilihan in kategori:
            return kategori[pilihan]

        print("Pilihan kategori tidak valid. Silakan coba lagi.")

def showMenu():
    print("\n================")
    print("  Money Manager ")
    print("================")
    print("1. Tambah Transaksi")
    print("2. Lihat Transaksi")
    print("3. Edit Transaksi")
    print("4. Hapus Transaksi")
    print("5. Lihat Saldo")
    print("6. Cari Transaksi")
    print("7. Laporan Keuangan")
    print("8. Filter Transaksi")
    print("9. Laporan Bulanan")
    print("0. Keluar")
    print("----------------")

def tambahTransaksi():
    print("\n=== Tambah Transaksi ===")
    tipeTransaksi = validasi.inputTipeTransaksi("Masukkan tipe transaksi (pemasukan/pengeluaran): ")

    # ID Baru
    idTerbesar = 0
    for t in transaksi:
        if t["id"] > idTerbesar:
            idTerbesar = t["id"]
    idBaru = idTerbesar + 1

    # Input Nominal
    nominal = validasi.inputNominal("Nominal : ")

    # Tanggal Transaksi
    tanggal = datetime.now().strftime("%d-%m-%Y")

    # Pilih Kategori
    kategori = pilihKategori()
    if kategori is None:
        return

    # Input Deskripsi
    while True:
        deskripsi = input("Deskripsi : ").strip()
        if deskripsi:
            break

        print("Deskripsi tidak boleh kosong")

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
    storage.saveData(transaksi)

    print("\nTransaksi berhasil ditambahkan!")
    print(f"ID Transaksi : {idBaru}")
    print(f"Tanggal      : {tanggal}")
    print(f"Tipe         : {tipeTransaksi}")
    print(f"Nominal      : {formatRupiah(nominal)}")
    print(f"Kategori     : {kategori}")
    print(f"Deskripsi    : {deskripsi}")

def lihatTransaksi():
    if not transaksi:
        print("Belum ada transaksi!")
        return
    
    print("\n=== Daftar Transaksi ===")

    for t in transaksi:
        tampilkanDetail(t)

def editTransaksi():
    print("\n=== Edit Transaksi ===")

    # Mencari transaksi berdasarkan ID
    try:
        idTransaksi = int(input("Masukkan ID transaksi : ").strip())
    except ValueError:
        print("ID transaksi harus berupa angka.")
        return

    t = cariTransaksi(idTransaksi)

    if t is None:
        print("Transaksi ID tidak ditemukan.")
        return

    while True:
        print("\n- Transaksi Saat Ini : ")
        tampilkanDetail(t)
        print("== Data yang dapat diubah ==")
        print("1. Nominal")
        print("2. Tipe")
        print("3. Kategori")
        print("4. Deskripsi")
        print("0. Selesai")
        print("----------------")
        pilihan = input("Pilih (0-4) : ")
        
        match pilihan:
            case "1":
                nominalBaru = validasi.inputNominal("Masukkan nominal baru : ")
                t["nominal"] = nominalBaru
                print("Nominal berhasil diubah.")

            case "2":
                tipeBaru = validasi.inputTipeTransaksi("Masukkan tipe transaksi baru (pemasukan/pengeluaran) : ")
                t["tipe"] = tipeBaru
                print("Tipe transaksi berhasil diubah.")
                continue

            case "3":
                kategoriBaru = pilihKategori()
                if kategoriBaru is None:
                    continue

                t["kategori"] = kategoriBaru
                print("Kategori berhasil diubah.")

            case "4":
                while True:
                    deskripsiBaru = input("Masukkan deskripsi baru : ").strip()
                    if deskripsiBaru:
                        t["deskripsi"] = deskripsiBaru
                        print("Deskripsi berhasil diubah.")
                        break

                    print("Deskripsi tidak boleh kosong ")
            case "0":
                storage.saveData(transaksi)
                print("Perubahan berhasil disimpan")
                break

            case _:
                print("Pilihan tidak valid.")

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
    while True:
        konfirmasi = input("Yakin anda ingin menghapus data ini? (y/n) : ")
        if konfirmasi == "y":
            transaksi.remove(t)
            storage.saveData(transaksi)
            print("Transaksi berhasil dihapus!")
            break
        
        elif konfirmasi == "n":
            print("Penghapusan dibatalkan.")
            break

        else:
            print("Input tidak valid! masukkan 'y' atau 'n'")

def lihatSaldo():
    totalPemasukan, totalPengeluaran, saldo = (keuangan.hitungSaldo(transaksi))
    print("\n=== Saldo Saat Ini ===")
    print(f"Total Pemasukan   : {formatRupiah(totalPemasukan)}")
    print(f"Total Pengeluaran : {formatRupiah(totalPengeluaran)}")
    print(f"Saldo Bersih      : {formatRupiah(saldo)}")

def laporanKeuangan():
    print("---- Laporan Keuangan ----")
    hasil = keuangan.laporanKeuangan(transaksi)
    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        return

    print("\n=== Ringkasan ===")
    print(f"Jumlah Transaksi  : {hasil["jumlahTransaksi"]}")
    print(f"Jumlah Pemasukan  : {hasil["jumlahPemasukan"]}")
    print(f"Jumlah Pengeluaran: {hasil["jumlahPengeluaran"]}")

    print("\n=== Keuangan ===")
    print(f"Total Pemasukan   : {formatRupiah(hasil["totalPemasukan"])}")
    print(f"Total Pengeluaran : {formatRupiah(hasil["totalPengeluaran"])}")
    print(f"Saldo Bersih      : {formatRupiah(hasil["saldo"])}")

    print("\n=== Pemasukan Berdasarkan Kategori ===")

    if not hasil["pemasukanKategori"]:
        print("Belum ada pemasukan.")
    else:
        for kategori, total in hasil["pemasukanKategori"].items():
            print(f"{kategori:<20}: {formatRupiah(total)}")

    print("\n=== Transaksi Terbesar ===")
    tampilkanDetail(hasil["transaksiTerbesar"])

    print("\n=== Pengeluaran Berdasarkan Kategori ===")

    if not hasil["pengeluaranKategori"]:
        print("Belum ada pengeluaran.")
    else:
        for kategori, total in hasil["pengeluaranKategori"].items():
            print(f"{kategori:<20}: {formatRupiah(total)}")

def filterTransaksi():
    while True:
        print("\n--- Filter Transaksi ---")
        print("1. Pemasukan")
        print("2. Pengeluaran")
        print("0. Kembali")
        pilihan = input("Pilih filter (0-2) : ").strip()
        match pilihan:
            case "1":
                tipeFilter = "pemasukan"
                break
            case "2":
                tipeFilter = "pengeluaran"
                break
            case "0":
                return
            case _:
                print("Tidak valid.")

    ditemukan = False
    for t in transaksi:
        if t["tipe"] == tipeFilter:
            tampilkanDetail(t)
            ditemukan = True

    if not ditemukan:
       print("Tidak ada transaksi yang sesuai.")

def laporanBulanan():
    print("\n=== Laporan Bulanan ===")

    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        return

    namaBulan = [
        "", "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus", "September", 
        "Oktober", "November", "Desember"
    ]
    while True:
        try:
            bulan = int(input("Masukkan bulan (1-12): "))
            tahun = int(input("Masukkan tahun (contoh: 2026): "))
            if bulan < 1 or bulan > 12:
                print("Bulan harus antara 1 dan 12.")
                continue

            if tahun < 1:
                print("Tidak ada tahun dibawah 0!")
                continue
            break
            
        except ValueError:
            print("Bulan dan tahun harus berupa angka.")
        
    # Variabel laporan
    totalPemasukan = 0
    totalPengeluaran = 0
    jumlahPemasukan = 0
    jumlahPengeluaran = 0

    pengeluaranKategori = {}
    transaksiBulan = []

    # Memfilter transaksi berdasarkan bulan dan tahun
    for t in transaksi:
        tanggal = None

        # Mendukung format tanggal lama dan baru
        for formatTanggal in ("%d-%m-%Y", "%d - %m - %Y"):
            try:
                tanggal = datetime.strptime(
                    t["tanggal"], formatTanggal
                )
                break
            except (ValueError, TypeError):
                continue

        # Lewati transaksi dengan tanggal yang tidak valid
        if tanggal is None:
            continue

        # Pastikan bulan dan tahun sesuai
        if tanggal.month != bulan or tanggal.year != tahun:
            continue

        transaksiBulan.append(t)

        if t["tipe"] == "pemasukan":
            totalPemasukan += t["nominal"]
            jumlahPemasukan += 1

        elif t["tipe"] == "pengeluaran":
            totalPengeluaran += t["nominal"]
            jumlahPengeluaran += 1

            kategori = t["kategori"]

            if kategori not in pengeluaranKategori:
                pengeluaranKategori[kategori] = 0

            pengeluaranKategori[kategori] += t["nominal"]

    # Periksa apakah transaksi ditemukan
    if len(transaksiBulan) == 0:
        print(
            f"Tidak ada transaksi pada "
            f"{namaBulan[bulan]} {tahun}."
        )
        return

    saldo = totalPemasukan - totalPengeluaran

    # Tampilkan laporan
    print(f"\n=== Laporan {namaBulan[bulan]} {tahun} ===")

    print("\n=== Ringkasan ===")
    print(f"Jumlah Transaksi   : {len(transaksiBulan)}")
    print(f"Jumlah Pemasukan   : {jumlahPemasukan}")
    print(f"Jumlah Pengeluaran : {jumlahPengeluaran}")

    print("\n=== Keuangan ===")
    print(f"Total Pemasukan    : {formatRupiah(totalPemasukan)}")
    print(f"Total Pengeluaran  : {formatRupiah(totalPengeluaran)}")
    print(f"Saldo Bersih       : {formatRupiah(saldo)}")

    print("\n=== Pengeluaran Berdasarkan Kategori ===")

    if len(pengeluaranKategori) == 0:
        print("Belum ada pengeluaran.")
    else:
        for kategori, total in pengeluaranKategori.items():
            print(f"{kategori:<20}: {formatRupiah(total)}")

    print("\n=== Daftar Transaksi Bulanan ===")

    for t in transaksiBulan:
        tampilkanDetail(t)

def main():
    while True:
        showMenu()
        choice = input("Pilih menu: ").strip()
        match choice:
            case "1":
                tambahTransaksi()
            case "2":
                lihatTransaksi()
            case "3":
                editTransaksi()
            case "4":
                hapusTransaksi()
            case "5":
                lihatSaldo()
            case "6":
                searchTransaksi()
            case "7":
                laporanKeuangan()
            case "8":
                filterTransaksi()
            case "9":
                laporanBulanan()
            case "0":
                print("\nTerima kasih telah menggunakan Money Manager!")
                break
            case _:
                print("Pilihan tidak tersedia.")

if __name__ == "__main__":
    main()