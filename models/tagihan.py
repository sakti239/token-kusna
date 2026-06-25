from models.database import db

class Tagihan(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    pelanggan_id = db.Column(
        db.Integer,
        db.ForeignKey("pelanggan.id")
    )

    pelanggan = db.relationship(
        "Pelanggan",
        backref="tagihan"
    )

    bulan = db.Column(db.String(20))
    tahun = db.Column(db.String(10))

    tagihan_pln = db.Column(db.Integer)
    admin = db.Column(db.Integer)

    total = db.Column(db.Integer)

    status = db.Column(
        db.String(30),
        default="Belum Dibayar"
    )

    tanggal_bayar = db.Column(db.String(30))