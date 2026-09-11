import requests
from config_loader import Config

class SportsPlugin:
    def __init__(self):
        # Reads cricket API key from config_master.yaml
        self.api_key = Config.get("apis.sports")
        self.base_url = "https://api.cricapi.com/v1/currentMatches"

    def get_scores(self, limit=5):
        """
        Fetch latest cricket scores.
        Default limit = 5 matches.
        """
        try:
            params = {"apikey": self.api_key}
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if response.status_code == 200 and "data" in data:
                matches = []
                for match in data["data"][:limit]:
                    matches.append({
                        "name": match.get("name"),
                        "status": match.get("status"),
                        "score": match.get("score", [])
                    })
                return {"status": "ok", "matches": matches}
            else:
                return {"status": "error", "message": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    sp = SportsPlugin()
    print(sp.get_scores(limit=5))
