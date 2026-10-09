import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def saveData(transaksi):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(transaksi, file, indent=4, ensure_ascii=False)
            print("Data berhasil disimpan !")
    except OSError as error:
        print(f"Gagal menyimpan data : {error}")

def loadData():
    global transaksi
    try:
        print("Lokasi data:", DATA_FILE)
        print("File ditemukan:", os.path.exists(DATA_FILE))
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            transaksi = json.load(file)
        print("Jumlah transaksi dimuat:", len(transaksi))
        print("Data berhasil dimuat.")
        return transaksi
    except FileNotFoundError:
        transaksi = []
        print("File data masih kosong")
    except json.JSONDecodeError:
        print("ERROR : Data JSON rusak atau tidak valid.")
        transaksi = []
    except OSError as error:
        print(f"Gagal menyimpan data : {error}")