from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from models.database import db
from models.pelanggan import Pelanggan
from models.tagihan import Tagihan
from datetime import datetime

app = Flask(__name__)

app.secret_key = "kusna-token-rahasia"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "sakti" and password == "Helaa239":

            session["admin"] = True

            return redirect("/admin")

        return "Username atau Password Salah"

    return render_template("login.html")
    
@app.route("/admin/pelanggan")
def admin_pelanggan():
    if not session.get("admin"):
        return redirect("/login")

    keyword = request.args.get("search")

    if keyword:

        semua_pelanggan = Pelanggan.query.filter(
            Pelanggan.nama.contains(keyword)
        ).all()

    else:

        semua_pelanggan = Pelanggan.query.all()

    return render_template(
    "admin_pelanggan.html",
    pelanggan=semua_pelanggan,
    active_page="pelanggan"
    )
    
@app.route(
    "/admin/tambah-pelanggan",
    methods=["GET","POST"]
)
def tambah_pelanggan():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":

        pelanggan = Pelanggan(
            nama=request.form["nama"],
            id_pln=request.form["id_pln"]
        )

        db.session.add(pelanggan)

        db.session.commit()

        return redirect("/admin/pelanggan")

    return render_template(
        "tambah_pelanggan.html"
    )
@app.route(
    "/admin/edit-pelanggan/<int:id>",
    methods=["GET","POST"]
)
def edit_pelanggan(id):
    if not session.get("admin"):
        return redirect("/login")

    pelanggan = Pelanggan.query.get_or_404(id)

    if request.method == "POST":

        pelanggan.nama = request.form["nama"]
        pelanggan.id_pln = request.form["id_pln"]
        pelanggan.hp = request.form["hp"]
        pelanggan.alamat = request.form["alamat"]

        db.session.commit()

        return redirect("/admin/pelanggan")

    return render_template(
        "edit_pelanggan.html",
        pelanggan=pelanggan
    )

@app.route("/admin/hapus-pelanggan/<int:id>")
def hapus_pelanggan(id):
    if not session.get("admin"):
        return redirect("/login")

    pelanggan = Pelanggan.query.get_or_404(id)

    db.session.delete(pelanggan)

    db.session.commit()

    return redirect("/admin/pelanggan")

@app.route("/admin/tagihan")
def admin_tagihan():

    if not session.get("admin"):
        return redirect("/login")

    keyword = request.args.get("search")
    status = request.args.get("status")
    bulan = request.args.get("bulan")

    query = Tagihan.query.join(Pelanggan)

    # Filter nama pelanggan
    if keyword:
        query = query.filter(
            Pelanggan.nama.contains(keyword)
        )

    # Filter status
    if status:
        query = query.filter(
            Tagihan.status == status
        )

    # Filter bulan
    if bulan:
        query = query.filter(
            Tagihan.bulan == bulan
        )

    semua_tagihan = query.all()

    return render_template(
        "admin_tagihan.html",
        tagihan=semua_tagihan,
        active_page="tagihan"
    )
    
@app.route("/admin/detail-tagihan/<int:id>")
def detail_tagihan(id):

    if not session.get("admin"):
        return redirect("/login")

    tagihan = Tagihan.query.get_or_404(id)

    return render_template(
        "detail_tagihan.html",
        tagihan=tagihan,
        active_page="tagihan"
    )
    
    
@app.route(
    "/admin/tambah-tagihan",
    methods=["GET", "POST"]
)
def tambah_tagihan():

    if not session.get("admin"):
        return redirect("/login")

    pelanggan = Pelanggan.query.all()

    if request.method == "POST":

        tagihan_pln = int(request.form["tagihan_pln"])

        admin = int(request.form["admin"])

        total = tagihan_pln + admin

        tagihan = Tagihan(

            pelanggan_id=request.form["pelanggan_id"],

            bulan=request.form["bulan"],

            tahun=request.form["tahun"],

            tagihan_pln=tagihan_pln,

            admin=admin,

            total=total,

            status="Belum Dibayar"

        )

        db.session.add(tagihan)

        db.session.commit()

        return redirect("/admin/tagihan")

    return render_template(
        "tambah_tagihan.html",
        pelanggan=pelanggan,
        active_page="tagihan"
    )

@app.route("/admin/lunas/<int:id>")
def lunas_tagihan(id):

    tagihan = Tagihan.query.get_or_404(id)

    tagihan.status = "Sudah Dibayar"

    tagihan.tanggal_bayar = datetime.now().strftime(
        "%d-%m-%Y"
    )

    db.session.commit()

    return redirect("/admin/tagihan")

@app.route("/cek-tagihan", methods=["GET","POST"])
def cek_tagihan():

    hasil = None
    pelanggan = None

    if request.method == "POST":

        nama = request.form.get("nama")

        pelanggan = Pelanggan.query.filter(
            Pelanggan.nama.contains(nama)
        ).first()

        if pelanggan:

            hasil = Tagihan.query.filter_by(
                pelanggan_id=pelanggan.id
            ).order_by(
                Tagihan.id.desc()
            ).first()

    return render_template(
        "cek_tagihan.html",
        hasil=hasil,
        pelanggan=pelanggan
    )
    
@app.route(
    "/admin/edit-tagihan/<int:id>",
    methods=["GET","POST"]
)
def edit_tagihan(id):

    if not session.get("admin"):
        return redirect("/login")

    tagihan = Tagihan.query.get_or_404(id)

    if request.method == "POST":

        tagihan.bulan = request.form["bulan"]
        tagihan.tahun = request.form["tahun"]

        tagihan.tagihan_pln = int(
            request.form["tagihan_pln"]
        )

        tagihan.admin = int(
            request.form["admin"]
        )

        tagihan.total = (
            tagihan.tagihan_pln +
            tagihan.admin
        )

        db.session.commit()

        return redirect("/admin/tagihan")

    return render_template(
        "edit_tagihan.html",
        tagihan=tagihan,
        active_page="tagihan"
    )    

@app.route("/admin/hapus-tagihan/<int:id>")
def hapus_tagihan(id):

    if not session.get("admin"):
        return redirect("/login")

    tagihan = Tagihan.query.get_or_404(id)

    db.session.delete(tagihan)

    db.session.commit()

    return redirect("/admin/tagihan")    
    
@app.route("/nota/<int:id>")
def nota(id):

    tagihan = Tagihan.query.get_or_404(id)

    pelanggan = Pelanggan.query.get(
        tagihan.pelanggan_id
    )

    return render_template(
        "nota.html",
        tagihan=tagihan,
        pelanggan=pelanggan
    )
    
@app.route("/admin")
def dashboard():
    
    if not session.get("admin"):
        return redirect("/login")

    total_pelanggan = Pelanggan.query.count()

    lunas = Tagihan.query.filter_by(
    status="Sudah Dibayar"
    ).count()

    belum = Tagihan.query.filter_by(
    status="Belum Dibayar"
    ).count()

    keuntungan = db.session.query(
    db.func.sum(Tagihan.admin)
    ).scalar() or 0

    tagihan_terbaru = Tagihan.query.order_by(
    Tagihan.id.desc()
    ).limit(5).all()

    return render_template(
    "dashboard.html",
    total_pelanggan=total_pelanggan,
    lunas=lunas,
    belum=belum,
    keuntungan=keuntungan,
    tagihan_terbaru=tagihan_terbaru,
    active_page="dashboard"
)

@app.route("/admin/keuangan")
def keuangan():

    if not session.get("admin"):
        return redirect("/login")

    bulan = request.args.get("bulan")
    tahun = request.args.get("tahun")

    query = Tagihan.query

    if bulan:
        query = query.filter(
            Tagihan.bulan == bulan
        )

    if tahun:
        query = query.filter(
            Tagihan.tahun == tahun
        )

    data = query.all()

    total_tagihan = sum(x.total for x in data)

    total_lunas = sum(
        x.total
        for x in data
        if x.status == "Sudah Dibayar"
    )

    total_belum = sum(
        x.total
        for x in data
        if x.status == "Belum Dibayar"
    )

    keuntungan = sum(
        x.admin
        for x in data
    )

    return render_template(
        "keuangan.html",
        total_tagihan=total_tagihan,
        total_lunas=total_lunas,
        total_belum=total_belum,
        keuntungan=keuntungan,
        bulan=bulan,
        tahun=tahun,
        active_page="keuangan"
    )
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)