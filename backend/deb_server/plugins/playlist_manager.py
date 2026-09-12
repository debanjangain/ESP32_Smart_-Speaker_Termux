from config_loader import Config

class PlaylistManager:
    def __init__(self):
        # Initialize empty playlist
        self.playlist = []

    def add_item(self, source, title, url):
        """
        Add a track/podcast/news item to playlist.
        """
        self.playlist.append({
            "source": source,
            "title": title,
            "url": url
        })
        return {"status": "ok", "message": f"Added {title} from {source}"}

    def remove_item(self, index):
        """
        Remove item by index.
        """
        try:
            removed = self.playlist.pop(index)
            return {"status": "ok", "message": f"Removed {removed['title']}"}
        except IndexError:
            return {"status": "error", "message": "Invalid index"}

    def list_items(self):
        """
        List all items in playlist.
        """
        return {"status": "ok", "playlist": self.playlist}

    def clear(self):
        """
        Clear entire playlist.
        """
        self.playlist = []
        return {"status": "ok", "message": "Playlist cleared"}

if __name__ == "__main__":
    pm = PlaylistManager()
    print(pm.add_item("YouTube", "Song A", "https://youtube.com/songA"))
    print(pm.add_item("Podcast", "Tech Talk", "https://podcast.com/techtalk"))
    print(pm.list_items())
    print(pm.remove_item(0))
    print(pm.list_items())
    print(pm.clear())
