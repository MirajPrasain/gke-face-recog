import pyttsx3
import os
import logging
from gtts import gTTS
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)

class TextToSpeechService:
    """Service for handling text-to-speech conversion."""
    
    def __init__(self, use_gtts=True):
        """
        Initialize the text-to-speech service.
        
        Args:
            use_gtts (bool): Whether to use Google TTS (True) or pyttsx3 (False)
        """
        self.use_gtts = use_gtts
        self.output_dir = os.path.join('static', 'audio')
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not use_gtts:
            # Initialize pyttsx3 engine
            try:
                self.engine = pyttsx3.init()
                self._setup_pyttsx3()
                logger.info("pyttsx3 TTS engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize pyttsx3: {str(e)}")
                self.engine = None
        else:
            logger.info("Using Google TTS (gTTS)")
    
    def _setup_pyttsx3(self):
        """Configure pyttsx3 settings."""
        if self.engine:
            # Set properties
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate - 50)  # Slower speech
            
            volume = self.engine.getProperty('volume')
            self.engine.setProperty('volume', 0.9)  # 90% volume
            
            # Try to set a more natural voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
    
    def text_to_speech(self, text: str, filename: str = None) -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text (str): Text to convert to speech
            filename (str, optional): Custom filename for the output file
            
        Returns:
            str: Path to the generated audio file or None if failed
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for TTS")
                return None
            
            # Generate filename if not provided
            if not filename:
                import time
                timestamp = int(time.time())
                filename = f"response_{timestamp}.mp3"
            
            output_path = os.path.join(self.output_dir, filename)
            
            if self.use_gtts:
                return self._gtts_convert(text, output_path)
            else:
                return self._pyttsx3_convert(text, output_path)
                
        except Exception as e:
            logger.error(f"Error in text_to_speech: {str(e)}")
            return None
    
    def _gtts_convert(self, text: str, output_path: str) -> Optional[str]:
        """
        Convert text to speech using Google TTS.
        
        Args:
            text (str): Text to convert
            output_path (str): Output file path
            
        Returns:
            str: Path to the generated file or None if failed
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to file
            tts.save(output_path)
            
            logger.info(f"TTS audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error with gTTS conversion: {str(e)}")
            return None
    
    def _pyttsx3_convert(self, text: str, output_path: str) -> Optional[str]:
        """
        Convert text to speech using pyttsx3.
        
        Args:
            text (str): Text to convert
            output_path (str): Output file path
            
        Returns:
            str: Path to the generated file or None if failed
        """
        try:
            if not self.engine:
                logger.error("pyttsx3 engine not initialized")
                return None
            
            # Change extension to wav for pyttsx3
            wav_path = os.path.splitext(output_path)[0] + '.wav'
            
            # Save to file
            self.engine.save_to_file(text, wav_path)
            self.engine.runAndWait()
            
            logger.info(f"TTS audio saved to: {wav_path}")
            return wav_path
            
        except Exception as e:
            logger.error(f"Error with pyttsx3 conversion: {str(e)}")
            return None
    
    def text_to_speech_with_options(self, text: str, language: str = 'en', 
                                  slow: bool = False, filename: str = None) -> Optional[str]:
        """
        Convert text to speech with additional options (gTTS only).
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (default: 'en')
            slow (bool): Whether to use slow speech (default: False)
            filename (str, optional): Custom filename for the output file
            
        Returns:
            str: Path to the generated audio file or None if failed
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for TTS")
                return None
            
            # Generate filename if not provided
            if not filename:
                import time
                timestamp = int(time.time())
                filename = f"response_{language}_{timestamp}.mp3"
            
            output_path = os.path.join(self.output_dir, filename)
            
            # Create gTTS object with options
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to file
            tts.save(output_path)
            
            logger.info(f"TTS audio with options saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in text_to_speech_with_options: {str(e)}")
            return None
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices (pyttsx3 only).
        
        Returns:
            list: List of available voice information
        """
        if not self.use_gtts and self.engine:
            try:
                voices = self.engine.getProperty('voices')
                voice_info = []
                for voice in voices:
                    voice_info.append({
                        'id': voice.id,
                        'name': voice.name,
                        'language': getattr(voice, 'languages', ['unknown'])[0] if hasattr(voice, 'languages') else 'unknown'
                    })
                return voice_info
            except Exception as e:
                logger.error(f"Error getting available voices: {str(e)}")
                return []
        else:
            # For gTTS, return supported languages
            return [
                {'id': 'en', 'name': 'English', 'language': 'en'},
                {'id': 'es', 'name': 'Spanish', 'language': 'es'},
                {'id': 'fr', 'name': 'French', 'language': 'fr'},
                {'id': 'de', 'name': 'German', 'language': 'de'},
                {'id': 'it', 'name': 'Italian', 'language': 'it'},
                {'id': 'pt', 'name': 'Portuguese', 'language': 'pt'},
                {'id': 'ru', 'name': 'Russian', 'language': 'ru'},
                {'id': 'ja', 'name': 'Japanese', 'language': 'ja'},
                {'id': 'ko', 'name': 'Korean', 'language': 'ko'},
                {'id': 'zh', 'name': 'Chinese', 'language': 'zh'}
            ]
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up old audio files.
        
        Args:
            max_age_hours (int): Maximum age of files to keep in hours
        """
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old audio file: {filename}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old files: {str(e)}")