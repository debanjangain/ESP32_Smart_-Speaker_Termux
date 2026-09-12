from config_loader import Config
import requests

class TTSProvider:
    def __init__(self):
        # Load TTS service config from config_master.yaml
        self.base_url = Config.get("apis.tts_url", default="https://api.elevenlabs.io/v1/tts")
        self.api_key = Config.get("apis.tts_key", default=None)
        self.voice_map = {
            "en": "EnglishVoice",
            "hi": "HindiVoice",
            "bn": "BengaliVoice"
        }

    def synthesize(self, text, lang="en"):
        """
        Convert text to speech in given language.
        """
        try:
            voice = self.voice_map.get(lang, "EnglishVoice")
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            payload = {"text": text, "voice": voice}
            response = requests.post(self.base_url, json=payload, headers=headers)
            if response.status_code == 200:
                return {"status": "ok", "audio": response.content}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    tts = TTSProvider()
    result = tts.synthesize("Hello Debanjan, this is your smart speaker.", lang="en")
    if result["status"] == "ok":
        with open("output_en.wav", "wb") as f:
            f.write(result["audio"])
        print("English TTS saved to output_en.wav")
    else:
        print("Error:", result["message"])
