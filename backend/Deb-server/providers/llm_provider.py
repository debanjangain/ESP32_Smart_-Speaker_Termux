from config_loader import Config
import requests

class LLMProvider:
    def __init__(self):
        # Load LLM configs from config_master.yaml
        self.llm_provider = Config.get("models.llm.provider", default="Qwen")
        self.llm_key = Config.get("models.llm.api_key", default=None)

        self.fallback_provider = Config.get("models.fallback_llm.provider", default="ChatGLM")
        self.fallback_key = Config.get("models.fallback_llm.api_key", default=None)

        self.base_urls = {
            "Qwen": "https://api.qwen.ai/v1/chat/completions",
            "ChatGLM": "https://api.chatglm.cn/v1/chat/completions"
        }

    def query_llm(self, text, provider=None, key=None):
        """
        Send text to given LLM provider.
        """
        try:
            provider = provider or self.llm_provider
            key = key or self.llm_key
            url = self.base_urls.get(provider)
            headers = {"Authorization": f"Bearer {key}"} if key else {}
            payload = {"messages": [{"
