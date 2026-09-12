from config_loader import Config
import requests

class LLMProvider:
    def __init__(self):
        # Load Gemini configs
        self.gemini_provider = Config.get("models.gemini.provider", default="Gemini")
        self.gemini_key = Config.get("models.gemini.api_key", default=None)

        # Load ChatGPT configs
        self.chatgpt_provider = Config.get("models.chatgpt.provider", default="ChatGPT")
        self.chatgpt_key = Config.get("models.chatgpt.api_key", default=None)

        # Load Qwen configs
        self.qwen_provider = Config.get("models.qwen.provider", default="Qwen")
        self.qwen_key = Config.get("models.qwen.api_key", default=None)

        # Base URLs for each provider
        self.base_urls = {
            "Gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "ChatGPT": "https://api.openai.com/v1/chat/completions",
            "Qwen": "https://api.qwen.ai/v1/chat/completions"
        }

    def query_llm(self, text, provider, key):
        """
        Send text to given LLM provider.
        """
        try:
            url = self.base_urls.get(provider)
            headers = {}
            payload = {}

            if provider == "Gemini":
                payload = {"contents": [{"parts": [{"text": text}]}]}
                headers = {"Content-Type": "application/json", "x-goog-api-key": key}
            elif provider == "ChatGPT":
                payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": text}]}
                headers = {"Authorization": f"Bearer {key}"}
            elif provider == "Qwen":
                payload = {"messages": [{"role": "user", "content": text}]}
                headers = {"Authorization": f"Bearer {key}"}

            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if provider == "Gemini":
                    reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
                elif provider == "ChatGPT":
                    reply = data.get("choices", [{}])[0].get("message", {}).get("content")
                else:  # Qwen
                    reply = data.get("choices", [{}])[0].get("message", {}).get("content")
                return {"status": "ok", "provider": provider, "reply": reply}
            else:
                return {"status": "error", "provider": provider, "message": response.text}
        except Exception as e:
            return {"status": "error", "provider": provider, "message": str(e)}

    def ask(self, text):
        """
        Try Gemini first, then ChatGPT, then Qwen.
        """
        # Gemini
        result = self.query_llm(text, self.gemini_provider, self.gemini_key)
        if result["status"] == "ok":
            return result

        # ChatGPT
        result = self.query_llm(text, self.chatgpt_provider, self.chatgpt_key)
        if result["status"] == "ok":
            return result

        # Qwen
        return self.query_llm(text, self.qwen_provider, self.qwen_key)

if __name__ == "__main__":
    llm = LLMProvider()
    response = llm.ask("Explain ESP32 smart speaker pipeline.")
    print(response)
