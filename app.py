import os
import time
import requests
from flask import Flask, jsonify, render_template, redirect, url_for, request

app = Flask(__name__)

START_TIME = time.time()

API_KEY = os.environ.get("CAT_API_KEY")
ANIMAL = "Cat"
CAT_URL = "https://api.thecatapi.com/v1/images/search"

saved_cats = []

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

        data = r.json()

        if r.status_code != 200:
            return render_template(
                "cat.html",
                error="Cat API error",
                image_url=None,
                animal=ANIMAL
            ), 502

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

    if image_url and image_url not in saved_cats:
        saved_cats.append(image_url)

    return redirect(url_for("saved"))


@app.route("/saved")
def saved():
    return render_template("saved.cat.html", saved_cats=saved_cats)


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

        data = r.json()

        if r.status_code != 200:
            return jsonify({
                "error": "Cat API error",
                "api_response": data,
            }), 502

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

@app.route("/saved")
def saved():
    return render_template("saved.html")


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200



@app.route("/status")
def status():
    uptime = round(time.time() - START_TIME, 2)

    return jsonify({
        "service": "Cat API Service",
        "uptime_seconds": uptime,
        "database": "not configured",
        "cat_api_configured": API_KEY is not None,
        "environment": os.environ.get("ENVIRONMENT", "development"),
    })


if __name__ == "__main__":
    app.run(debug=True)
