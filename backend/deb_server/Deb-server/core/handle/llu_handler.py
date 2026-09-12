import asyncio
from providers.llm.llm_provider import LLMProvider

# Initialize once
llm = LLMProvider()

async def process_llu(websocket, message):
    """
    Handle LLM (Language Understanding Unit) requests from ESP32.
    Expected format: LLU:<query>
    Example: LLU:What is the capital of India?
    """
    try:
        print("[LLU] Received LLM request:", message)

        # Remove prefix
        query = message.replace("LLU:", "", 1).strip()

        # Ask the LLM provider (Gemini → ChatGPT → Qwen fallback)
        result = llm.ask(query)

        if result["status"] == "ok":
            reply = f"[LLU:{result['provider']}] {result['reply']}"
        else:
            reply = f"[LLU] Error: {result['message']}"

        await websocket.send(reply)

    except Exception as e:
        error_msg = f"[LLU] Error processing request: {str(e)}"
        print(error_msg)
        await websocket.send(error_msg)
