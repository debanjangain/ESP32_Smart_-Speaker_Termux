import asyncio
from plugins.youtube_music import play_youtube_song
from plugins.jiosaavn_music import play_jiosaavn_song
from plugins.gaana_music import play_gaana_song

async def process_music(websocket, message):
    """
    Handle music requests from ESP32.
    Expected format: MUSIC:<provider>:<song name>
    Example: MUSIC:YOUTUBE:Despacito
    """
    try:
        print("[MUSIC] Received music request:", message)

        # Split the message into parts
        parts = message.split(":")
        if len(parts) < 3:
            await websocket.send("[MUSIC] Invalid request format")
            return

        provider = parts[1].upper()
        song_name = parts[2]

        # Route to the correct plugin
        if provider == "YOUTUBE":
            result = play_youtube_song(song_name)
        elif provider == "JIOSAAVN":
            result = play_jiosaavn_song(song_name)
        elif provider == "GAANA":
            result = play_gaana_song(song_name)
        else:
            result = "[MUSIC] Unknown provider"

        # Send back the result (e.g., stream URL or confirmation)
        await websocket.send(result)

    except Exception as e:
        error_msg = f"[MUSIC] Error processing request: {str(e)}"
        print(error_msg)
        await websocket.send(error_msg)
