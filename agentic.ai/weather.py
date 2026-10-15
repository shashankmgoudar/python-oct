import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_city_coordinates(city):
    """Find a city's latitude and longitude using Open-Meteo's free geocoding API."""
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        return None

    place = results[0]
    return {
        "name": place["name"],
        "country": place.get("country", "Unknown country"),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
    }


def get_weather(latitude, longitude):
    """Fetch current weather and today's forecast from Open-Meteo."""
    response = requests.get(
        API_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "is_day,precipitation,rain,weather_code,wind_speed_10m"
            ),
            "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset",
            "timezone": "auto",
            "forecast_days": 1,
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def main():
    print("=" * 42)
    print("       CITY WEATHER REPORT")
    print("Powered by Open-Meteo (free API)")
    print("=" * 42)

    while True:
        city = input("\nEnter a city name (or 'q' to quit): ").strip()

        if city.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            break

        if not city:
            print("Please enter a city name.")
            continue
        