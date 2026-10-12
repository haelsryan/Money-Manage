import os
import json
import sqlite3

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
DATABASE_FILE = os.path.join(DATABASE_DIR, "money_manager.db")
SCHEMA_FILE = os.path.join(DATABASE_DIR, "data.sql")

def _openDatabase():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
            connection.executescript(file.read())
        return connection
    except (OSError, sqlite3.Error):
        connection.close()
        raise

def _importLegacyData(connection):
    migrated = connection.execute(
        "SELECT value FROM app_metadata WHERE key = 'legacy_json_migrated'"
    ).fetchone()
    if migrated is not None:
        return

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                transaksi = json.load(file)
            if isinstance(transaksi, list):
                connection.executemany(
                    """INSERT OR IGNORE INTO transactions
                       (id, tanggal, tipe, nominal, kategori, deskripsi)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    [
                        (
                            item["id"],
                            item["tanggal"],
                            item["tipe"],
                            item["nominal"],
                            item["kategori"],
                            item["deskripsi"],
                        )
                        for item in transaksi
                    ],
                )
        except (OSError, json.JSONDecodeError, KeyError, TypeError, sqlite3.Error) as error:
            print(f"Gagal mengimpor data JSON: {error}")

    connection.execute(
        "INSERT INTO app_metadata (key, value) VALUES ('legacy_json_migrated', '1')"
    )

def saveData(transaksi):
    connection = None
    try:
        connection = _openDatabase()
        with connection:
            connection.execute("DELETE FROM transactions")
            connection.executemany(
                """INSERT INTO transactions
                   (id, tanggal, tipe, nominal, kategori, deskripsi)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    (
                        item["id"],
                        item["tanggal"],
                        item["tipe"],
                        item["nominal"],
                        item["kategori"],
                        item["deskripsi"],
                    )
                    for item in transaksi
                ],
            )
        print("Data berhasil disimpan !")
    except (OSError, sqlite3.Error, KeyError, TypeError) as error:
        print(f"Gagal menyimpan data : {error}")
    finally:
        if connection is not None:
            connection.close()

def loadData():
    connection = None
    try:
        connection = _openDatabase()
        connection.execute(
            """CREATE TABLE IF NOT EXISTS app_metadata (
                   key TEXT PRIMARY KEY,
                   value TEXT NOT NULL
               )"""
        )
        with connection:
            _importLegacyData(connection)
        rows = connection.execute(
            """SELECT id, tanggal, tipe, nominal, kategori, deskripsi
               FROM transactions ORDER BY id"""
        ).fetchall()
        transaksi = [dict(row) for row in rows]
        print("Data berhasil dimuat.")
        return transaksi
    except (OSError, sqlite3.Error) as error:
        print(f"Gagal memuat data : {error}")
        return []
    finally:
        if connection is not None:
            connection.close()