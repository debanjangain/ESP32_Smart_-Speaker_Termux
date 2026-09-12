import asyncio
import websockets
from core.connection_handler import handle_connection

async def start_server(host="0.0.0.0", port=8765):
    """
    Start the WebSocket server.
    - host: IP address to bind (default: all interfaces)
    - port: Port number (default: 8765)
    """
    async def handler(websocket, path):
        # Delegate each connection to connection_handler
        await handle_connection(websocket, path)

    # Create the server
    server = await websockets.serve(handler, host, port)
    print(f"[CORE] WebSocket server running at ws://{host}:{port}")

    # Keep server alive
    await server.wait_closed()
