# 🌤 Skycast — Flask Weather Dashboard

A weather dashboard built with Flask that shows current conditions and a 5-day forecast for any city.

## Features
- 🔍 Search any city worldwide
- 🌡 Current temperature, feels-like, humidity, wind, pressure, visibility
- 📅 5-day forecast with icons
- ⚡ Powered by OpenWeatherMap API

---

## Setup Instructions

### 1. Get a free API key
1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to **API Keys** in your profile and copy your key
4. ⚠️ New keys take ~10 minutes to activate

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Open `app.py` and replace `YOUR_API_KEY_HERE` with your actual key:
```python
API_KEY = "your_actual_key_here"
```

Or set it as an environment variable (more secure):
```bash
# Mac/Linux
export OPENWEATHER_API_KEY="your_key_here"

# Windows
set OPENWEATHER_API_KEY=your_key_here
```

### 4. Run the app
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Project Structure
```
weather-dashboard/
├── app.py              ← Flask routes & API calls
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── templates/
    └── index.html      ← Frontend (HTML + CSS + JS)
```

## What You'll Learn
- **API Integration** — calling an external HTTP API with `urllib`
- **JSON Parsing** — extracting data from nested JSON responses
- **Flask Routing** — `@app.route` with query parameters
- **Frontend ↔ Backend** — using `fetch()` in JS to call your Flask endpoint
- **Environment Variables** — keeping API keys secure
