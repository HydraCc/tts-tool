# engine/models/coqui_xtts.py

from engine.models import BaseTTS
from TTS.api import TTS as CoquiTTSAPI
import torch
import torchaudio
import os
import io

class CoquiXTTS(BaseTTS):
    def load_model(self):
        model_name = self.config.get("model_name", "tts_models/en/ljspeech/tacotron2-DDC")
        vocoder_name = self.config.get("vocoder_name", None)

        if vocoder_name:
            self.tts = CoquiTTSAPI(model_name, vocoder_name=vocoder_name)
        else:
            self.tts = CoquiTTSAPI(model_name)

        self.speaker = self.config.get("speaker", None)
        self.language = self.config.get("language", None)
        self.sample_rate = self.config.get("sample_rate", 22050)

    def synthesize(self, text: str) -> bytes:
        if not hasattr(self, 'tts'):
            raise RuntimeError("Model not loaded. Call load_model() first.")

        wav = self.tts.tts(text, speaker=self.speaker, language=self.language)
        wav_tensor = torch.tensor(wav).unsqueeze(0)  # Shape: [1, N]
        buffer = self._tensor_to_bytes(wav_tensor)
        return buffer

    def save_audio(self, audio_bytes: bytes, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        audio_tensor, _ = torchaudio.load(io.BytesIO(audio_bytes))
        torchaudio.save(path, audio_tensor, sample_rate=self.sample_rate)

    def _tensor_to_bytes(self, tensor: torch.Tensor) -> bytes:
        buffer = io.BytesIO()
        torchaudio.save(buffer, tensor, sample_rate=self.sample_rate, format="wav")
        return buffer.getvalue()
