import requests
from flask import Flask, jsonify

app = Flask(__name__)

# -----------------------
# HARD-CODED CONFIG (DEMO ONLY)
# -----------------------
API_KEY = "live_nd5ftUYkwJRLVWcOyHHUAK9tzvrqCTqi5APyWJBCIti0jxtwEa6Q06uBcv5twr7P"
ANIMAL = "Cat"
CAT_URL = "https://api.thecatapi.com/v1/images/search"


@app.route("/")
def index():
    return {"message": "Cat API running"}


@app.route("/cat")
def weather():
    try:
        r = requests.get(
            CAT_URL,
            params={
                "q": ANIMAL,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=5,
        )

        data = r.json()

        # Handle API-level errors
        if r.status_code != 200:
            return jsonify({
                "error": "Cat API error",
                "api_response": data,
            }), 502

        return jsonify({
            "city": ANIMAL,
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


