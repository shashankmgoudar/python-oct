
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail"
}


def get_weather(city):
    # Find city coordinates
    response = requests.get(
        GEO_URL,
        params={"name": city, "count": 1, "language": "en"},
        timeout=15
    )
    response.raise_for_status()

    places = response.json().get("results", [])

    if not places:
        print("City not found. Please try again.")
        return

    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Get weather information
    response = requests.get(
        API_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,precipitation,"
                "weather_code,wind_speed_10m"
            ),
            "daily": (
                "temperature_2m_max,temperature_2m_min,"
                "sunrise,sunset"
            ),
            "timezone": "auto",
            "forecast_days": 1
        },
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    current = data["current"]
    daily = data["daily"]

    condition = WEATHER_CODES.get(
        current["weather_code"], "Other conditions"
    )

    # Display weather report
    print("\n========== WEATHER REPORT ==========")
    print(f"City: {place['name']}, {place.get('country', '')}")
    print(f"Condition: {condition}")
    print(f"Temperature: {current['temperature_2m']} °C")
    print(f"Feels like: {current['apparent_temperature']} °C")
    print(f"Humidity: {current['relative_humidity_2m']}%")
    print(f"Wind speed: {current['wind_speed_10m']} km/h")
    print(f"Precipitation: {current['precipitation']} mm")
    print(f"Today's maximum: {daily['temperature_2m_max'][0]} °C")
    print(f"Today's minimum: {daily['temperature_2m_min'][0]} °C")
    print(f"Sunrise: {daily['sunrise'][0]}")
    print(f"Sunset: {daily['sunset'][0]}")
    print("====================================")


def main():
    print("CITY WEATHER REPORT")

    while True:
        city = input(
            "\nEnter city name (or q to quit): "
        ).strip()

        if city.lower() in ("q", "quit", "exit"):
            print("Thank you for using the weather app!")
            break

        if not city:
            print("Please enter a valid city name.")
            continue

        try:
            get_weather(city)
        except requests.RequestException:
            print("Network error. Check your internet connection.")
        except (KeyError, IndexError, ValueError):
            print("Unable to process weather data. Try again.")


if __name__ == "__main__":
    main()


```python
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #9face6);
            text-align: center;
            padding: 80px 15px;
        }

        .container {
            background: white;
            max-width: 400px;
            margin: auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px #777;
        }

        h1 {
            color: #333;
        }

        input {
            padding: 12px;
            width: 85%;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin: 15px 0;
            box-sizing: border-box;
        }

        button {
            padding: 12px 25px;
            background: #4169e1;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        button:hover {
            background: #2748a5;
        }

        .result {
            margin-top: 25px;
            padding: 15px;
            background: #eef5ff;
            border-radius: 10px;
            line-height: 2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather App</h1>
        <p>Check the current weather of any city</p>

        <form method="POST">
            <input type="text" name="city"
                   placeholder="Enter city name" required>
            <br>
            <button type="submit">Get Weather</button>
        </form>

        {% if result %}
        <div class="result">
            {{ result | safe }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            geo_response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1},
                timeout=10
            )
            geo_response.raise_for_status()
            places = geo_response.json().get("results", [])

            if not places:
                result = "City not found. Please try again."
            else:
                place = places[0]

                weather_response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": place["latitude"],
                        "longitude": place["longitude"],
                        "current": (
                            "temperature_2m,"
                            "relative_humidity_2m,"
                            "wind_speed_10m"
                        )
                    },
                    timeout=10
                )
                weather_response.raise_for_status()
                weather = weather_response.json()["current"]

                result = (
                    f"City: {place['name']}<br>"
                    f"Temperature: {weather['temperature_2m']} °C<br>"
                    f"Humidity: {weather['relative_humidity_2m']}%<br>"
                    f"Wind Speed: {weather['wind_speed_10m']} km/h"
                )

        except (requests.RequestException, KeyError, ValueError):
            result = "Unable to get weather. Check your internet and try again."

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(debug=True)




