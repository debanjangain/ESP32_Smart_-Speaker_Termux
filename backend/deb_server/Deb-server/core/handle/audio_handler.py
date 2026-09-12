import asyncio

async def process_audio(websocket, message):
    """
    Handle audio messages from ESP32.
    Expected format: AUDIO:<data or command>
    """
    try:
        # For now, just confirm receipt
        print("[AUDIO] Received audio message:", message)

        # Later: you can expand this to decode audio and send to ASR provider
        # Example: text = asr_model.transcribe(audio_bytes)

        await websocket.send("[AUDIO] Audio processed successfully")
    except Exception as e:
        error_msg = f"[AUDIO] Error processing audio: {str(e)}"
        print(error_msg)
        await websocket.send(error_msg)
