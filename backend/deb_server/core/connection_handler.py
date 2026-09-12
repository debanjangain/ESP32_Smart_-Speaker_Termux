from core.handle.audio_handler import process_audio
from core.handle.music_handler import process_music
from core.handle.llu_handler import process_llu

async def handle_connection(websocket, path):
    """
    Handle each ESP32 connection.
    Routes messages to the correct handler based on prefix.
    """
    async for message in websocket:
        print(f"[CORE] Received: {message}")

        if message.startswith("AUDIO:"):
            await process_audio(websocket, message)
        elif message.startswith("MUSIC:"):
            await process_music(websocket, message)
        elif message.startswith("LLU:"):
            await process_llu(websocket, message)
        else:
            await websocket.send("[CORE] Unknown request type")
