from flask import Flask, render_template

app = Flask(__name__)

BOBOT = {"A": 4.0, "AB": 3.5, "B": 3.0, "BC": 2.5, "C": 2.0, "D": 1.0, "E": 0.0}
BADGE = {"A": "success", "AB": "info", "B": "warning", "BC": "secondary"}

BIODATA = {
    "nama": "Eliazar Yasta Prarindra",
    "nbi": "1482500005",
    "prodi": "Sistem dan Teknologi Informasi",
}

DAFTAR_NILAI = [
    {"kode": "14823192", "matkul": "Arsitektur dan Organisasi Komputer", "semester": 2, "sks": 2, "nilai": "AB"},
    {"kode": "14823372", "matkul": "Statistika dan Probabilitas", "semester": 2, "sks": 2, "nilai": "A"},
    {"kode": "14823274", "matkul": "Pemrograman Berorientasi Objek", "semester": 2, "sks": 4, "nilai": "A"},
    {"kode": "14823313", "matkul": "Sistem Basis Data", "semester": 2, "sks": 3, "nilai": "AB"},
    {"kode": "14823393", "matkul": "Interaksi Manusia Komputer", "semester": 2, "sks": 3, "nilai": "B"},
    {"kode": "14823333", "matkul": "Algoritma dan Struktur Data", "semester": 2, "sks": 3, "nilai": "A"},
    {"kode": "14823153", "matkul": "Teknologi Informasi dan Aplikasi Bisnis Berkembang", "semester": 2, "sks": 3, "nilai": "B"},
]


def olah_nilai():
    """Tambahkan N.K (sks x bobot) dan warna badge ke tiap mata kuliah."""
    return [
        {**m, "nk": m["sks"] * BOBOT[m["nilai"]], "badge": BADGE.get(m["nilai"], "secondary")}
        for m in DAFTAR_NILAI
    ]

def rekap():
    data = olah_nilai()
    total_sks = sum(m["sks"] for m in data)
    total_nk = sum(m["nk"] for m in data)
    ipk = round(total_nk / total_sks + 1e-9, 2)
    return total_sks, total_nk, ipk

@app.route("/")
def index():
    return render_template("index.html", bio=BIODATA)

@app.route("/nilai")
def nilai():
    total_sks, total_nk, ipk = rekap()
    return render_template(
        "nilai.html",
        daftar=olah_nilai(),
        total_sks=total_sks,
        total_nk=total_nk,
        ipk=ipk,
    )

@app.route("/admin")
def admin_dashboard():
    data = olah_nilai()
    total_sks, total_nk, ipk = rekap()
    statistik = [
        {"label": "Mata Kuliah", "nilai": len(data), "warna": "primary", "ikon": "📚"},
        {"label": "Total SKS", "nilai": total_sks, "warna": "success", "ikon": "🧮"},
        {"label": "IPK Semester 2", "nilai": f"{ipk:.2f}", "warna": "warning", "ikon": "🎓"},
        {"label": "Nilai A", "nilai": sum(1 for m in data if m["nilai"] == "A"), "warna": "info", "ikon": "⭐"},
    ]
    return render_template(
        "admin/dashboard.html",
        statistik=statistik,
        terbaru=data[:5],
        admin_nama=BIODATA["nama"],
    )


@app.route("/admin/matkul")
def admin_matkul():
    return render_template("admin/matkul.html", daftar=olah_nilai(), admin_nama=BIODATA["nama"])


if __name__ == "__main__":
    app.run(debug=True)