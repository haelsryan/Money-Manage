def inputNominal(pesan):
    while True:
        try:
            nominal = int(input(pesan))
            if nominal <= 0:
                print("Angka tidak boleh minus!")
                continue
            return nominal
        except ValueError:
            print("Tidak Valid! masukkan angka.")

def inputTipeTransaksi(pesan):
    while True:
        tipe = input(pesan).strip().lower()
        if tipe in ("pemasukan", "pengeluaran"):
            return tipe

        print("Tidak tervalidasi tipe transaksi, masukkan 'pemasukan' atau 'pengeluaran'.")