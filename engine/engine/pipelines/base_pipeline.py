"""
Base Pipeline Module for TTS Processing

This module provides an abstract base class for implementing processing pipelines for various models.
It defines the common interface for handling the complete workflow.
Examples:
- TTS Pipeline: Processes text input through a TTS model to generate audio output.
- STT Pipeline: Converts audio input to text using a speech-to-text model. 
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union


class BasePipeline(ABC):
    """
    Abstract base class for pipelines.
    
    This class defines the standard interface for TTS pipelines that orchestrate
    the complete text-to-speech workflow. It handles model loading, component
    initialization, and the main processing flow from input to output.
    
    Attributes:
        model_name  : Name or identifier of the TTS model to be used.
        config      : Configuration dictionary containing pipeline-specific
                                settings and parameters.
    
    Example:
        ```python
        class MyTTSPipeline(BasePipeline):
            def load_components(self):
                # Load TTS model, vocoder, text processor, etc.
                self.tts_model = load_model(self.model_name)
                self.vocoder = load_vocoder()
                
            def process(self, input_data, save_path: str = None):
                # Process text through the complete pipeline
                text = self.preprocess_text(input_data)
                mel_spec = self.tts_model.synthesize(text)
                audio = self.vocoder.generate(mel_spec)
                if save_path:
                    self.save_audio(audio, save_path)
                return audio
        ```
    """
    
    def __init__(self, model_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TTS pipeline with model name and configuration.
        
        Args:
            model_name (str): Name or identifier of the TTS model to use.
                            This could be a model path, HuggingFace model ID,
                            or any other identifier recognized by the pipeline.
            config (Optional[Dict[str, Any]]): Configuration dictionary containing
                                             pipeline-specific parameters such as:
                                             - Sample rate
                                             - Model parameters
                                             - Processing options
                                             - Output format settings
                                             If None, an empty dictionary is used.
        """
        self.model_name = model_name
        self.config = config or {}

    @abstractmethod
    def load_components(self) -> None:
        """
        Load and initialize all necessary models and processing components.
        
        This method should handle the loading and initialization of all components
        required for the TTS pipeline, including but not limited to:
        - Main TTS model (text-to-mel spectrogram)
        - Vocoder (mel spectrogram-to-audio)
        - Text preprocessing tools
        - Audio post-processing tools
        - Any other pipeline-specific components
        
        The method should ensure all components are properly loaded and ready
        for processing before returning.
        
        Raises:
            NotImplementedError: Must be implemented by subclasses.
            RuntimeError: If any component fails to load.
            FileNotFoundError: If model files are not found.
            
        Example:
            ```python
            def load_components(self):
                self.text_processor = TextProcessor()
                self.tts_model = TTSModel.load(self.model_name)
                self.vocoder = Vocoder.load(self.config.get('vocoder_path'))
                self.audio_processor = AudioProcessor(self.config)
            ```
        """
        pass

    @abstractmethod
    def process(self, input_data: Union[str, Dict[str, Any]], save_path: Optional[str] = None) -> Any:
        """
        Main processing interface that converts input to audio output.
        
        This is the primary method that orchestrates the complete TTS workflow.
        It takes input data (typically text) and processes it through the entire
        pipeline to generate audio output.
        
        Args:
            input_data (Union[str, Dict[str, Any]]): Input data to be processed.
                                                   Can be:
                                                   - Simple text string
                                                   - Dictionary with text and metadata
                                                   - Structured input with processing options
            save_path (Optional[str]): File path where the generated audio should be saved.
                                     If provided, the audio will be written to disk.
                                     If None, only the audio data is returned.
        
        Returns:
            Any: Generated audio data. The exact format depends on the implementation:
                - Could be raw audio bytes
                - NumPy array with audio samples
                - Audio tensor
                - File path if saved to disk
        
        Raises:
            NotImplementedError: Must be implemented by subclasses.
            ValueError: If input_data is invalid or malformed.
            RuntimeError: If processing fails at any stage.
            IOError: If save_path is provided but file cannot be written.
            
        Example:
            ```python
            def process(self, input_data, save_path=None):
                # Preprocess input
                text = self.extract_text(input_data)
                text = self.text_processor.normalize(text)
                
                # Generate mel spectrogram
                mel_spec = self.tts_model.text_to_mel(text)
                
                # Convert to audio
                audio = self.vocoder.mel_to_audio(mel_spec)
                
                # Post-process audio
                audio = self.audio_processor.enhance(audio)
                
                # Save if path provided
                if save_path:
                    self.save_audio(audio, save_path)
                    
                return audio
            ```
        """
        pass