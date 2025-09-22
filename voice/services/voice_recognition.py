import speech_recognition as sr
import os
import logging
from pydub import AudioSegment
from pydub.utils import which

logger = logging.getLogger(__name__)

class VoiceRecognitionService:
    """Service for handling speech-to-text conversion."""
    
    def __init__(self):
        """Initialize the voice recognition service."""
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
    def speech_to_text(self, audio_file_path):
        """
        Convert speech in audio file to text.
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            # Convert audio to WAV format if needed
            wav_path = self._convert_to_wav(audio_file_path)
            
            # Load the audio file
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                # Record the audio
                audio_data = self.recognizer.record(source)
            
            # Recognize speech using Google Web Speech API
            try:
                text = self.recognizer.recognize_google(audio_data)
                logger.info(f"Successfully recognized speech: {text}")
                
                # Clean up converted file if it's different from original
                if wav_path != audio_file_path and os.path.exists(wav_path):
                    os.remove(wav_path)
                    
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand the audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Could not request results from Google Speech Recognition service: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech_to_text: {str(e)}")
            return None
    
    def _convert_to_wav(self, audio_file_path):
        """
        Convert audio file to WAV format if needed.
        
        Args:
            audio_file_path (str): Path to the original audio file
            
        Returns:
            str: Path to the WAV file
        """
        try:
            # Get file extension
            file_ext = os.path.splitext(audio_file_path)[1].lower()
            
            # If already WAV, return as is
            if file_ext == '.wav':
                return audio_file_path
            
            # Convert to WAV
            wav_path = os.path.splitext(audio_file_path)[0] + '_converted.wav'
            
            # Load and convert audio
            if file_ext == '.mp3':
                audio = AudioSegment.from_mp3(audio_file_path)
            elif file_ext == '.ogg':
                audio = AudioSegment.from_ogg(audio_file_path)
            elif file_ext == '.m4a':
                audio = AudioSegment.from_file(audio_file_path, "m4a")
            elif file_ext == '.flac':
                audio = AudioSegment.from_file(audio_file_path, "flac")
            elif file_ext == '.webm':
                audio = AudioSegment.from_file(audio_file_path, "webm")
            else:
                # Try generic conversion
                audio = AudioSegment.from_file(audio_file_path)
            
            # Export as WAV
            audio.export(wav_path, format="wav")
            logger.info(f"Converted {audio_file_path} to {wav_path}")
            
            return wav_path
            
        except Exception as e:
            logger.error(f"Error converting audio file: {str(e)}")
            # Return original path if conversion fails
            return audio_file_path
    
    def speech_to_text_with_options(self, audio_file_path, language='en-US'):
        """
        Convert speech to text with language options.
        
        Args:
            audio_file_path (str): Path to the audio file
            language (str): Language code (default: 'en-US')
            
        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            # Convert audio to WAV format if needed
            wav_path = self._convert_to_wav(audio_file_path)
            
            # Load the audio file
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                # Record the audio
                audio_data = self.recognizer.record(source)
            
            # Recognize speech using Google Web Speech API with language
            try:
                text = self.recognizer.recognize_google(audio_data, language=language)
                logger.info(f"Successfully recognized speech in {language}: {text}")
                
                # Clean up converted file if it's different from original
                if wav_path != audio_file_path and os.path.exists(wav_path):
                    os.remove(wav_path)
                    
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand the audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Could not request results from Google Speech Recognition service: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech_to_text_with_options: {str(e)}")
            return None