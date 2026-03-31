import os
import time
import requests
from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

START_TIME = time.time()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "cats.db")
DB_URL = f"sqlite:///{DB_PATH}"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

API_KEY = os.environ.get("CAT_API_KEY")
ANIMAL = "Cat"
CAT_URL = "https://api.thecatapi.com/v1/images/search"


class SavedCat(db.Model):
    __tablename__ = "saved_cat"

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return f"<SavedCat {self.image_url}>"


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cat")
def cat():
    if not API_KEY:
        return render_template(
            "cat.html",
            error="CAT_API_KEY is not configured",
            image_url=None,
            animal=ANIMAL
        ), 500

    try:
        r = requests.get(
            CAT_URL,
            headers={"x-api-key": API_KEY},
            timeout=5,
        )
        r.raise_for_status()

        data = r.json()

        if not isinstance(data, list) or not data or "url" not in data[0]:
            return render_template(
                "cat.html",
                error="Unexpected Cat API response",
                image_url=None,
                animal=ANIMAL
            ), 502

        return render_template(
            "cat.html",
            animal=ANIMAL,
            image_url=data[0]["url"],
            error=None
        )

    except requests.RequestException as e:
        return render_template(
            "cat.html",
            error=f"Failed to contact Cat API service: {str(e)}",
            image_url=None,
            animal=ANIMAL
        ), 503


@app.route("/save_cat")
def save_cat():
    image_url = request.args.get("image_url")

    if not image_url:
        return "Missing image_url", 400

    try:
        existing_cat = SavedCat.query.filter_by(image_url=image_url).first()

        if not existing_cat:
            new_cat = SavedCat(image_url=image_url)
            db.session.add(new_cat)
            db.session.commit()

        return redirect(url_for("saved"))

    except Exception as e:
        db.session.rollback()
        return f"Database error: {e}", 500


@app.route("/saved")
def saved():
    saved_cats = SavedCat.query.order_by(SavedCat.id.desc()).all()
    return render_template("saved.cat.html", saved_cats=saved_cats)


@app.route("/debug/saved_cats")
def debug_saved_cats():
    cats = SavedCat.query.order_by(SavedCat.id.desc()).all()
    return jsonify([
        {"id": cat.id, "image_url": cat.image_url}
        for cat in cats
    ])


@app.route("/api/cat")
def api_cat():
    if not API_KEY:
        return jsonify({"error": "CAT_API_KEY is not configured"}), 500

    try:
        r = requests.get(
            CAT_URL,
            headers={"x-api-key": API_KEY},
            timeout=5,
        )
        r.raise_for_status()

        data = r.json()

        if not isinstance(data, list) or not data or "url" not in data[0]:
            return jsonify({
                "error": "Unexpected Cat API response",
                "api_response": data,
            }), 502

        return jsonify({
            "animal": ANIMAL,
            "image_url": data[0]["url"]
        })

    except requests.RequestException as e:
        return jsonify({
            "error": "Failed to contact Cat API service",
            "details": str(e),
        }), 503


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/status")
def status():
    uptime = round(time.time() - START_TIME, 2)

    try:
        db.session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {e}"

    return jsonify({
        "service": "Cat API Service",
        "uptime_seconds": uptime,
        "database": db_status,
        "database_path": DB_PATH,
        "cat_api_configured": API_KEY is not None,
        "environment": os.environ.get("ENVIRONMENT", "development"),
    })


if __name__ == "__main__":
    app.run(debug=True)