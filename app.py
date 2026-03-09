from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json
import os
from ph_data import PH_DATA

app = Flask(__name__)

API_KEY  = os.environ.get("OPENWEATHER_API_KEY", "apikey")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SkycastApp/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        if e.code == 404: return None, "City not found."
        if e.code == 401: return None, "Invalid API key."
        return None, f"Service error ({e.code})."
    except Exception as e:
        return None, "Could not connect to weather service."


@app.route("/")
def index():
    return render_template("index.html")


# ── Philippine geo endpoints ───────────────────────────
@app.route("/ph/regions")
def ph_regions():
    return jsonify(sorted(PH_DATA.keys()))


@app.route("/ph/provinces")
def ph_provinces():
    region = request.args.get("region", "")
    return jsonify(sorted(PH_DATA.get(region, {}).keys()))


@app.route("/ph/cities")
def ph_cities():
    region   = request.args.get("region", "")
    province = request.args.get("province", "")
    return jsonify(sorted(PH_DATA.get(region, {}).get(province, [])))


# ── Weather endpoint ───────────────────────────────────
@app.route("/weather")
def weather():
    city    = request.args.get("city", "").strip()
    country = request.args.get("country", "PH").strip()

    if not city:
        return jsonify({"error": "Please provide a city name."}), 400

    # Strip " City" suffix — OWM often knows "Isabela" but not "Isabela City"
    clean = city
    for suffix in [" City", " city"]:
        if clean.endswith(suffix):
            clean = clean[:-len(suffix)].strip()
            break

    # Try multiple query variants in order until one works
    attempts = [
        f"q={urllib.parse.quote(city)},{country}",
        f"q={urllib.parse.quote(clean)},{country}",
        f"q={urllib.parse.quote(city)}",
        f"q={urllib.parse.quote(clean)}",
    ]
    # Deduplicate while preserving order
    seen = set()
    unique_attempts = []
    for a in attempts:
        if a not in seen:
            seen.add(a)
            unique_attempts.append(a)

    current_data = None
    for query in unique_attempts:
        data, _ = fetch_json(f"{BASE_URL}/weather?{query}&appid={API_KEY}&units=metric")
        if data:
            current_data = data
            break

    if not current_data:
        return jsonify({"error": f"'{city}' not found. Try a nearby larger city."}), 404

    # Forecast using confirmed coordinates
    lat = current_data["coord"]["lat"]
    lon = current_data["coord"]["lon"]
    forecast_data, err = fetch_json(
        f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    if err:
        return jsonify({"error": err}), 404

    daily = {}
    for item in forecast_data["list"]:
        date = item["dt_txt"].split(" ")[0]
        hour = item["dt_txt"].split(" ")[1]
        if date not in daily and hour >= "11:00:00":
            daily[date] = {
                "date":        date,
                "temp_min":    item["main"]["temp_min"],
                "temp_max":    item["main"]["temp_max"],
                "description": item["weather"][0]["description"],
                "icon":        item["weather"][0]["icon"],
            }

    return jsonify({
        "city":        current_data["name"],
        "country":     current_data["sys"]["country"],
        "lat":         lat,
        "lon":         lon,
        "temperature": round(current_data["main"]["temp"]),
        "feels_like":  round(current_data["main"]["feels_like"]),
        "humidity":    current_data["main"]["humidity"],
        "pressure":    current_data["main"]["pressure"],
        "wind_speed":  round(current_data["wind"]["speed"] * 3.6, 1),
        "description": current_data["weather"][0]["description"].title(),
        "icon":        current_data["weather"][0]["icon"],
        "visibility":  current_data.get("visibility", 0) // 1000,
        "forecast":    list(daily.values())[:5],
    })


if __name__ == "__main__":
    app.run(debug=True)