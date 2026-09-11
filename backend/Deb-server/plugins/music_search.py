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
        # Example: using yt-dlp JSON search
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
        # Placeholder: JioSaavn API integration
        # Replace with actual API call
        return [{"title": f"JioSaavn result {i+1}", "url": f"https://www.jiosaavn.com/{query}/{i}"} for i in range(limit)]

    def search_gaana(self, query, limit=5):
        if not self.gaana_enabled:
            return []
        # Placeholder: Gaana API integration
        # Replace with actual API call
        return [{"title": f"Gaana result {i+1}", "url": f"https://gaana.com/{query}/{i}"} for i in range(limit)]

    def search_all(self, query, limit=5):
        results
