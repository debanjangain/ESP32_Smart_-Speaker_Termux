import feedparser
from config_loader import Config

class NewsPlugin:
    def __init__(self):
        # Reads RSS feed URL from config_master.yaml
        self.feed_url = Config.get("apis.news_rss", default="https://news.google.com/rss")

    def get_headlines(self, limit=10):
        """
        Fetch latest headlines from configured RSS feed.
        Default limit = 10.
        """
        try:
            feed = feedparser.parse(self.feed_url)
            headlines = []
            for entry in feed.entries[:limit]:
                headlines.append({
                    "title": entry.title,
                    "link": entry.link
                })
            return {"status": "ok", "headlines": headlines}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    np = NewsPlugin()
    print(np.get_headlines(limit=10))
