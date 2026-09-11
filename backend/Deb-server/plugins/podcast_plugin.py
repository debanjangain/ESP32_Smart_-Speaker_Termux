import requests
from config_loader import Config

class PodcastPlugin:
    def __init__(self):
        # Reads PodcastIndex API base URL from config_master.yaml
        self.base_url = Config.get("apis.podcast", default="https://api.podcastindex.org")
        # Normally PodcastIndex requires API key + secret headers
        self.api_key = Config.get("apis.podcast_key", default=None)
        self.api_secret = Config.get("apis.podcast_secret", default=None)

    def search_podcast(self, query, limit=5):
        """
        Search podcasts by keyword.
        """
        try:
            headers = {}
            if self.api_key and self.api_secret:
                headers = {
                    "X-API-Key": self.api_key,
                    "X-API-Secret": self.api_secret
                }
            response = requests.get(f"{self.base_url}/api/1.0/search/byterm",
                                    params={"q": query},
                                    headers=headers)
            data = response.json()
            if response.status_code == 200 and "feeds" in data:
                results = []
                for feed in data["feeds"][:limit]:
                    results.append({
                        "title": feed.get("title"),
                        "url": feed.get("url"),
                        "description": feed.get("description")
                    })
                return {"status": "ok", "podcasts": results}
            else:
                return {"status": "error", "message": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    pp = PodcastPlugin()
    print(pp.search_podcast("technology", limit=5))
