from models.database import db

class Pelanggan(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nama = db.Column(db.String(100))

    id_pln = db.Column(db.String(50))