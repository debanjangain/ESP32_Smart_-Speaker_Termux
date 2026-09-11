from config_loader import Config
import requests

class MusicSearch:
    def __init__(self):
        # Check which services are enabled in config_master.yaml
        self.youtube_enabled = Config.get("apis.youtube", default="disabled") == "yt-dlp"
        self.jiosaavn_enabled = Config.get("apis.jiosaavn", default="disabled") == "enabled"
        self.gaana_enabled = Config.get("apis.gaana", default="disabled") == "enabled"

    def search_youtube(self, query, limit=5):
        if not self.youtube_enabled:
            return []
        import subprocess, json
        cmd = ["yt-dlp", f"ytsearch{limit}:{query}", "--dump-json"]
        results = []
        try:
            output = subprocess.check_output(cmd, text=True)
            for line in output.strip().split("\n"):
                data = json.loads(line)
                results.append({
                    "title": data.get("title"),
                    "url": data.get("webpage_url")
                })
        except Exception as e:
            results.append({"error": str(e)})
        return results

    def search_jiosaavn(self, query, limit=5):
        if not self.jiosaavn_enabled:
            return []
        # Placeholder: replace with real JioSaavn API integration
        return [{"title": f"JioSaavn result {i+1}", "url": f"https://www.jiosaavn.com/{query}/{i}"} for i in range(limit)]

    def search_gaana(self, query, limit=5):
        if not self.gaana_enabled:
            return []
        # Placeholder: replace with real Gaana API integration
        return [{"title": f"Gaana result {i+1}", "url": f"https://gaana.com/{query}/{i}"} for i in range(limit)]

    def search_all(self, query, limit=5):
        results = {}
        if self.youtube_enabled:
            results["youtube"] = self.search_youtube(query, limit)
        if self.jiosaavn_enabled:
            results["jiosaavn"] = self.search_jiosaavn(query, limit)
        if self.gaana_enabled:
            results["gaana"] = self.search_gaana(query, limit)
        return {"status": "ok", "results": results}

if __name__ == "__main__":
    ms = MusicSearch()
    # Example: pass any query dynamically
    user_query = input("Enter search term: ")
    print(ms.search_all(user_query, limit=3))
