from engine.pipelines import TTSPipeline

pipeline = TTSPipeline(model_name="coqui_xtts", config={"model_name": "tts_models/en/ljspeech/tacotron2-DDC"})
pipeline.load_components()
audio_bytes = pipeline.process("Hello, world!", save_path="sample_data/output.wav")
