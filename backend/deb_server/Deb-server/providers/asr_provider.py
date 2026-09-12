from config_loader import Config
import requests

class ASRProvider:
    def __init__(self):
        # Load ASR service config
        self.base_url = Config.get("apis.asr_url", default="https://api.openai.com/v1/audio/transcriptions")
        self.api_key = Config.get("apis.asr_key", default=None)
        self.lang_map = {
            "en": "en-US",
            "hi": "hi-IN",
            "bn": "bn-IN"
        }

    def transcribe(self, audio_file, lang="en"):
        """
        Transcribe audio file into text for given language.
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            files = {"file": open(audio_file, "rb")}
            data = {"language": self.lang_map.get(lang, "en-US")}
            response = requests.post(self.base_url, headers=headers, files=files, data=data)
            if response.status_code == 200:
                return {"status": "ok", "text": response.json().get("text")}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    asr = ASRProvider()
    result = asr.transcribe("sample_hi.wav", lang="hi")
    print(result)
