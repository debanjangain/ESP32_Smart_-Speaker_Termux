import feedparser
from config_loader import Config

class NewsPlugin:
    def __init__(self):
        # Always expects a list of feeds
        self.feeds = Config.get("apis.news_feeds", default=[])

    def get_headlines(self, limit=10):
        results = []
        try:
            for feed_url in self.feeds:
                feed = feedparser.parse(feed_url)
                headlines = []
                for entry in feed.entries[:limit]:
                    headlines.append({
                        "title": entry.title,
                        "link": entry.link
                    })
                results.append({
                    "feed": feed_url,
                    "headlines": headlines
                })
            return {"status": "ok", "feeds": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    np = NewsPlugin()
    data = np.get_headlines(limit=10)
    for feed in data.get("feeds", []):
        print(f"\nFeed: {feed['feed']}")
        for h in feed["headlines"]:
            print(" -", h["title"])
