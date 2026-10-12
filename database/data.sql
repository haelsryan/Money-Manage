CREATE TABLE IF NOT EXISTS transactions (
	id INTEGER PRIMARY KEY,
	tanggal TEXT NOT NULL,
	tipe TEXT NOT NULL CHECK (tipe IN ('pemasukan', 'pengeluaran')),
	nominal INTEGER NOT NULL CHECK (nominal > 0),
	kategori TEXT NOT NULL,
	deskripsi TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_transactions_tanggal
	ON transactions (tanggal);
