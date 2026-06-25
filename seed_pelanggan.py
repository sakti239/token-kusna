from app import app
from models.database import db
from models.pelanggan import Pelanggan

data = [
    ("524030156015", "AHMADI"),
    ("524030155948", "BIMO"),
    ("524030161628", "DARORI"),
    ("524051115544", "DUL MUCHID"),
    ("524030161602", "ENI NINGSIH"),
    ("524030495253", "HARJO MULYONO"),
    ("524030662869", "JUDIYONO"),
    ("524031129348", "JUMINI"),
    ("524030667099", "KOERUDIN"),
    ("524031051691", "KUSAENI"),
    ("524030938072", "MARKAMAH"),
    ("524030158149", "MASJID"),
    ("524030380184", "MITRO WIHARJO"),
    ("524031048901", "MUHADI"),
    ("524051117436", "MUHAMMAD KHURI"),
    ("524051096246", "MUJI WIBOWO"),
    ("524030444974", "MUKSAM"),
    ("524030852522", "SAJINEM"),
    ("524030664171", "SAKBINI"),
    ("524030155989", "SARI"),
    ("524030158164", "SUMARDI"),
    ("524030748976", "SRI JOKO SISWANTO"),
    ("524030156007", "SRIYADI"),
    ("524031081586", "SUDIMAN"),
    ("524030803395", "SLAMET"),
    ("524010931661", "SUMARNO"),
    ("524030662877", "SUMARSIH"),
    ("524030677965", "TEGUH MULYONO"),
    ("524030155906", "TUKIMAN"),
    ("524030284344", "WAHAP"),
    ("524030667111", "WALADI"),
    ("524030156271", "WALIMIN"),
    ("524030978920", "ZAENAL ARIFIN"),
    ("524030213562", "SUKADI"),
    ("524030995635", "NOMO"),
]

with app.app_context():
    for id_pln, nama in data:
        pelanggan = Pelanggan(
            nama=nama,
            id_pln=id_pln
        )
        db.session.add(pelanggan)

    db.session.commit()

print("Data pelanggan berhasil ditambahkan!")