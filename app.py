from flask import Flask, render_template, request, redirect, jsonify, url_for, session, flash
import json, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"  # ubah untuk keamanan

DATA_FILE = "data.json"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"  # ubah sesuai keinginan


# ----------------- UTILITAS -----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------- HALAMAN UTAMA -----------------
@app.route("/")
def index():
    items = load_data()
    return render_template("index.html", items=items)


# ----------------- LOGIN / LOGOUT -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Login berhasil ✅", "success")
            return redirect(url_for("admin"))
        flash("Username atau password salah ❌", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Berhasil logout 👋", "success")
    return redirect(url_for("login"))


# ----------------- ADMIN DASHBOARD -----------------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    items = load_data()
    return render_template("admin.html", items=items)


@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect(url_for("login"))

    items = load_data()
    emoji = request.form.get("emoji", "🍽️").strip() or "🍽️"
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("admin"))

    image_file = request.files.get("image")
    image_path = ""
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)

    new_item = {
        "id": str(uuid.uuid4()),
        "emoji": emoji,
        "name": name,
        "desc": "",
        "rating": 0,
        "image": image_path.replace("\\", "/")
    }
    items.append(new_item)
    save_data(items)
    return redirect(url_for("admin"))


@app.route("/admin/edit/<id>", methods=["POST"])
def admin_edit(id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    items = load_data()
    for item in items:
        if item["id"] == id:
            item["emoji"] = request.form.get("emoji", item["emoji"])
            item["name"] = request.form.get("name", item["name"])
            img_file = request.files.get("image")
            if img_file and allowed_file(img_file.filename):
                filename = secure_filename(img_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                img_file.save(image_path)
                item["image"] = image_path.replace("\\", "/")
    save_data(items)
    return redirect(url_for("admin"))


@app.route("/admin/delete/<id>", methods=["POST"])
def admin_delete(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    items = [i for i in load_data() if i["id"] != id]
    save_data(items)
    return redirect(url_for("admin"))


# ----------------- API UNTUK USER -----------------
@app.route("/api/update/<id>", methods=["POST"])
def api_update(id):
    payload = request.get_json() or {}
    items = load_data()
    for it in items:
        if it["id"] == id:
            if "desc" in payload:
                it["desc"] = str(payload["desc"])
            if "rating" in payload:
                try:
                    it["rating"] = float(payload["rating"])
                except:
                    pass
            break
    save_data(items)
    return jsonify({"status": "ok"})


@app.route("/api/items")
def api_items():
    return jsonify(load_data())


# ----------------- JALANKAN APP -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
