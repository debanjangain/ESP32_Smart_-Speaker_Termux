import requests
from config_loader import Config

class WeatherPlugin:
    def __init__(self):
        # Reads API key from config_master.yaml
        self.api_key = Config.get("apis.openweather_key")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str):
        """
        Fetch weather for any city dynamically.
        """
        try:
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                return {
                    "status": "ok",
                    "city": city,
                    "temp": data["main"]["temp"],
                    "desc": data["weather"][0]["description"]
                }
            else:
                return {"status": "error", "message": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    wp = WeatherPlugin()
    # Example: change city dynamically
    print(wp.get_weather("Delhi"))
    print(wp.get_weather("Kolkata"))
    print(wp.get_weather("Kanpur"))
