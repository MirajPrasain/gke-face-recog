from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import our custom services
from services.voice_recognition import VoiceRecognitionService
from services.gemini_service import GeminiService
from services.text_to_speech import TextToSpeechService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions for audio uploads
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'flac', 'webm'}

# Initialize services
voice_service = VoiceRecognitionService()
gemini_service = GeminiService()
tts_service = TextToSpeechService()

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('static/demo.html')

@app.route('/api', methods=['GET'])
def home():
    """Health check endpoint."""
    return jsonify({
        'status': 'success',
        'message': 'Voice Recognition API with Gemini-2.5-Flash is running!',
        'endpoints': {
            '/voice-command': 'POST - Upload audio file for voice recognition and response',
            '/text-command': 'POST - Send text command and get voice response',
            '/health': 'GET - Health check'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'voice-recognition-api'})

@app.route('/voice-command', methods=['POST'])
def voice_command():
    """
    Main endpoint for voice recognition and response.
    Accepts audio file, converts to text, processes with Gemini, and returns both text and audio response.
    """
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"Audio file saved: {filepath}")
            
            # Step 1: Convert speech to text
            recognized_text = voice_service.speech_to_text(filepath)
            if not recognized_text:
                # Clean up uploaded file
                os.remove(filepath)
                return jsonify({'error': 'Could not recognize speech from audio'}), 400
            
            logger.info(f"Recognized text: {recognized_text}")
            
            # Step 2: Get response from Gemini
            gemini_response = gemini_service.get_response(recognized_text)
            if not gemini_response:
                # Clean up uploaded file
                os.remove(filepath)
                return jsonify({'error': 'Could not get response from Gemini'}), 500
            
            logger.info(f"Gemini response: {gemini_response}")
            
            # Step 3: Convert response to speech
            audio_response_path = tts_service.text_to_speech(gemini_response)
            if not audio_response_path:
                # Clean up uploaded file
                os.remove(filepath)
                return jsonify({'error': 'Could not generate audio response'}), 500
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Return the response
            return jsonify({
                'status': 'success',
                'recognized_text': recognized_text,
                'response_text': gemini_response,
                'audio_response_url': f'/download-audio/{os.path.basename(audio_response_path)}'
            })
        
        else:
            return jsonify({'error': 'Invalid file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
    
    except Exception as e:
        logger.error(f"Error in voice_command: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/text-command', methods=['POST'])
def text_command():
    """
    Endpoint for text-based commands.
    Accepts text input, processes with Gemini, and returns both text and audio response.
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        input_text = data['text'].strip()
        if not input_text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        logger.info(f"Input text: {input_text}")
        
        # Step 1: Get response from Gemini
        gemini_response = gemini_service.get_response(input_text)
        if not gemini_response:
            return jsonify({'error': 'Could not get response from Gemini'}), 500
        
        logger.info(f"Gemini response: {gemini_response}")
        
        # Step 2: Convert response to speech
        audio_response_path = tts_service.text_to_speech(gemini_response)
        if not audio_response_path:
            return jsonify({'error': 'Could not generate audio response'}), 500
        
        # Return the response
        return jsonify({
            'status': 'success',
            'input_text': input_text,
            'response_text': gemini_response,
            'audio_response_url': f'/download-audio/{os.path.basename(audio_response_path)}'
        })
    
    except Exception as e:
        logger.error(f"Error in text_command: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    """Download generated audio file."""
    try:
        filepath = os.path.join('static', 'audio', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}")
        return jsonify({'error': 'Could not download audio file'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static/audio', exist_ok=True)
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )