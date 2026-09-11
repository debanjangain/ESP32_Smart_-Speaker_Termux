from config_loader import Config
import requests

class LLMProvider:
    def __init__(self):
        # Load primary LLM configs
        self.llm_provider = Config.get("models.llm.provider", default="Qwen")
        self.llm_key = Config.get("models.llm.api_key", default=None)

        # Load fallback LLM configs
        self.fallback_provider = Config.get("models.fallback_llm.provider", default="ChatGLM")
        self.fallback_key = Config.get("models.fallback_llm.api_key", default=None)

        # Load Gemini configs
        self.gemini_provider = Config.get("models.gemini.provider", default="Gemini")
        self.gemini_key = Config.get("models.gemini.api_key", default=None)

        # Base URLs for each provider
        self.base_urls = {
            "Qwen": "https://api.qwen.ai/v1/chat/completions",
            "ChatGLM": "https://api.chatglm.cn/v1/chat/completions",
            "Gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        }

    def query_llm(self, text, provider, key):
        """
        Send text to given LLM provider.
        """
        try:
            url = self.base_urls.get(provider)
            headers = {"Authorization": f"Bearer {key}"} if key else {}
            payload = {"messages": [{"role": "user", "content": text}]}

            # Gemini uses a slightly different payload
            if provider == "Gemini":
                payload = {"contents": [{"parts": [{"text": text}]}]}
                headers = {"Content-Type": "application/json", "x-goog-api-key": key}

            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if provider == "Gemini":
                    reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
                else:
                    reply = data.get("choices", [{}])[0].get("message", {}).get("content")
                return {"status": "ok", "provider": provider, "reply": reply}
            else:
                return {"status": "error", "provider": provider, "message": response.text}
        except Exception as e:
            return {"status": "error", "provider": provider, "message": str(e)}

    def ask(self, text):
        """
        Try primary LLM, fallback to ChatGLM, then Gemini if needed.
        """
        # Primary
        result = self.query_llm(text, self.llm_provider, self.llm_key)
        if result["status"] == "ok":
            return result

        # Fallback
        result = self.query_llm(text, self.fallback_provider, self.fallback_key)
        if result["status"] == "ok":
            return result

        # Gemini as last fallback
        return self.query_llm(text, self.gemini_provider, self.gemini_key)

if __name__ == "__main__":
    llm = LLMProvider()
    response = llm.ask("Explain ESP32 smart speaker architecture.")
    print(response)
