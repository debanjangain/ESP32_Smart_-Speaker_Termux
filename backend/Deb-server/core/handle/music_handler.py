import asyncio
from plugins.music_search import MusicSearch
from plugins.playlist_manager import PlaylistManager
from plugins.youtube_music import YouTubeMusic

# Initialize once
music_search = MusicSearch()
playlist = PlaylistManager()
youtube = YouTubeMusic()

async def process_music(websocket, message):
    """
    Handle music requests from ESP32.
    Expected formats:
      MUSIC:SEARCH:<query>
      MUSIC:PLAYLIST:ADD:<source>:<title>:<url>
      MUSIC:PLAYLIST:LIST
      MUSIC:YOUTUBE:<query>
    """
    try:
        print("[MUSIC] Received:", message)
        parts = message.split(":")

        if len(parts) < 2:
            await websocket.send("[MUSIC] Invalid request format")
            return

        action = parts[1].upper()

        # Search across all providers
        if action == "SEARCH" and len(parts) >= 3:
            query = parts[2]
            results = music_search.search_all(query, limit=3)
            await websocket.send(str(results))

        # Playlist management
        elif action == "PLAYLIST":
            if len(parts) >= 3:
                sub_action = parts[2].upper()
                if sub_action == "ADD" and len(parts) >= 6:
                    source, title, url = parts[3], parts[4], parts[5]
                    result = playlist.add_item(source, title, url)
                    await websocket.send(str(result))
                elif sub_action == "LIST":
                    result = playlist.list_items()
                    await websocket.send(str(result))
                elif sub_action == "CLEAR":
                    result = playlist.clear()
                    await websocket.send(str(result))
                else:
                    await websocket.send("[MUSIC] Invalid playlist command")
            else:
                await websocket.send("[MUSIC] Missing playlist command")

        # Direct YouTube streaming
        elif action == "YOUTUBE" and len(parts) >= 3:
            query = parts[2]
            result = youtube.play(query)
            await websocket.send(str(result))

        else:
            await websocket.send("[MUSIC] Unknown action")

    except Exception as e:
        error_msg = f"[MUSIC] Error: {str(e)}"
        print(error_msg)
        await websocket.send(error_msg)
