import requests
from flask import Flask, jsonify

app = Flask(__name__)

# -----------------------
# HARD-CODED CONFIG (DEMO ONLY)
# -----------------------
API_KEY = "81cb6ce9dfe2460132197b153919419e"  # Add your OpenWeatherMap API key here
CITY = "Cork"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def index():
    return {"message": "Weather API running"}


@app.route("/weather")
def weather():
    try:
        r = requests.get(
            WEATHER_URL,
            params={
                "q": CITY,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=5,
        )

        data = r.json()

        # Handle API-level errors
        if r.status_code != 200:
            return jsonify({
                "error": "Weather API error",
                "api_response": data,
            }), 502

        return jsonify({
            "city": CITY,
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


