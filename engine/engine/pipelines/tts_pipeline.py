from engine.pipelines import BasePipeline
from engine.models import coqui_xtts  # Add more models as needed

MODEL_MAP = {
    "coqui_xtts": coqui_xtts.CoquiXTTS,
    # Add "chatterbox"
    # Add "dia"
}

class TTSPipeline(BasePipeline):
    def load_components(self):
        if self.model_name not in MODEL_MAP:
            raise ValueError(f"Unsupported TTS model: {self.model_name}")
        self.tts_model = MODEL_MAP[self.model_name](self.config)
        self.tts_model.load_model()

    def process(self, input_data: str, save_path: str = None) -> bytes:
        audio = self.tts_model.synthesize(input_data)
        if save_path:
            self.tts_model.save_audio(audio, save_path)
        return audio
