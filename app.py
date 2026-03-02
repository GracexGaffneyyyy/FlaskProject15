import requests
from flask import Flask, jsonify

app = Flask(__name__)

# -----------------------
# HARD-CODED CONFIG (DEMO ONLY)
# -----------------------
API_KEY = "hKT8XfnxESwFxDGgpvANmivKuKZROrIH0SkqFetq"  # Add your OpenWeatherMap API key here
Astronaut = "Neil Armstrong"
NASA_URL = "https://api.nasa.gov/"


@app.route("/")
def index():
    return {"message": "Nasa API running"}


@app.route("/nasa")
def nasa():
    try:
        r = requests.get(
            NASA_URL,
            params={
                "q": astronaut,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=5,
        )

        data = r.json()

        # Handle API-level errors
        if r.status_code != 200:
            return jsonify({
                "error": "NASA API error",
                "api_response": data,
            }), 502

        return jsonify({
            "city": Astronaut,
            "temperature": data["main"]["temp"],
            "conditions": data["weather"][0]["description"],
        })

    except requests.RequestException as e:
        return jsonify({
            "error": "Failed to contact weather service",
            "details": str(e),
        }), 503


if __name__ == "__main__":
    app.run(debug=True)


