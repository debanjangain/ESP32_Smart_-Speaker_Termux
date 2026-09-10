import subprocess
from config_loader import Config

class YouTubeMusic:
    def __init__(self):
        # Load yt-dlp path from config
        self.tool = Config.get("apis.youtube", default="yt-dlp")
        # Preferred runtime for Termux
        self.runtime = Config.get("apis.youtube_runtime", default="quickjs")

    def stream(self, query: str):
        """
        Get direct streaming URL for a YouTube search query.
        Returns the signed stream URL (temporary).
        """
        try:
            cmd = [
                self.tool,
                "--js-runtime", self.runtime,
                "-f", "bestaudio",
                "--get-url",
                f"ytsearch:{query}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            url = result.stdout.strip()
            if url:
                return {"status": "ok", "title": query, "stream_url": url}
            else:
                return {"status": "error", "message": "No stream URL found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fallback_download(self, query: str):
        """
        Fallback: download audio file, play, then auto-delete.
        """
        try:
            cmd = [
                self.tool,
                "--js-runtime", self.runtime,
                "-f", "bestaudio",
                "-o", "last_song.%(ext)s",
                f"ytsearch:{query}"
            ]
            subprocess.run(cmd, capture_output=True, text=True)
            return {"status": "ok", "file": "last_song.mp3"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def play(self, query: str):
        """
        Try streaming first, fallback to download+delete if needed.
        """
        stream_result = self.stream(query)
        if stream_result.get("status") == "ok":
            return stream_result
        else:
            return self.fallback_download(query)
