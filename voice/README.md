# Voice Recognition API with Gemini-2.5-Flash

A Python Flask API that provides voice recognition and intelligent responses using Google's Gemini-2.5-Flash AI model. The API can process voice commands, convert speech to text, generate intelligent responses, and convert responses back to speech.

## Features

- 🎤 **Voice Recognition**: Convert audio files to text using Google Speech Recognition
- 🤖 **AI Responses**: Generate intelligent responses using Gemini-2.5-Flash
- 🔊 **Text-to-Speech**: Convert AI responses to speech audio
- 🌐 **RESTful API**: Easy-to-use HTTP endpoints
- 📁 **Multiple Audio Formats**: Support for WAV, MP3, OGG, M4A, FLAC, WebM
- 🗣️ **Voice Navigation**: Specialized handling for navigation commands
- 🔄 **Contextual Conversations**: Maintain conversation context

## Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini (get from [Google AI Studio](https://aistudio.google.com/app/apikey))
- Internet connection for speech recognition and AI responses

## Installation

1. **Clone or download the project:**
   ```bash
   cd /Users/satyamregmi/Desktop/gke-hack
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

5. **Create necessary directories:**
   ```bash
   mkdir -p static/audio uploads
   ```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

### API Endpoints

#### 1. Health Check
```http
GET /
GET /health
```

#### 2. Voice Command Processing
```http
POST /voice-command
Content-Type: multipart/form-data
```

**Parameters:**
- `audio`: Audio file (WAV, MP3, OGG, M4A, FLAC, WebM)

**Response:**
```json
{
  "status": "success",
  "recognized_text": "What's the weather like today?",
  "response_text": "I'd be happy to help you with weather information...",
  "audio_response_url": "/download-audio/response_1234567890.mp3"
}
```

#### 3. Text Command Processing
```http
POST /text-command
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "How do I get to the nearest coffee shop?"
}
```

**Response:**
```json
{
  "status": "success",
  "input_text": "How do I get to the nearest coffee shop?",
  "response_text": "To find the nearest coffee shop...",
  "audio_response_url": "/download-audio/response_1234567890.mp3"
}
```

#### 4. Download Audio Response
```http
GET /download-audio/<filename>
```

### Example Usage with cURL

#### Upload and process voice command:
```bash
curl -X POST \
  http://localhost:5000/voice-command \
  -F "audio=@path/to/your/audio.wav"
```

#### Send text command:
```bash
curl -X POST \
  http://localhost:5000/text-command \
  -H "Content-Type: application/json" \
  -d '{"text": "Navigate to the nearest restaurant"}'
```

### Example Usage with Python

```python
import requests

# Text command example
def send_text_command(text):
    url = "http://localhost:5000/text-command"
    data = {"text": text}
    response = requests.post(url, json=data)
    return response.json()

# Voice command example
def send_voice_command(audio_file_path):
    url = "http://localhost:5000/voice-command"
    with open(audio_file_path, 'rb') as f:
        files = {'audio': f}
        response = requests.post(url, files=files)
    return response.json()

# Usage
result = send_text_command("What's the weather like?")
print(result)
```

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for Gemini (required)
- `FLASK_ENV`: Flask environment (development/production)
- `PORT`: Server port (default: 5000)
- `DEFAULT_LANGUAGE`: Default language for speech recognition (default: en-US)
- `USE_GTTS`: Use Google TTS instead of pyttsx3 (default: true)
- `MAX_FILE_SIZE_MB`: Maximum upload file size (default: 16)
- `AUDIO_CLEANUP_HOURS`: Hours to keep generated audio files (default: 24)

### Supported Audio Formats

- WAV (recommended for best quality)
- MP3
- OGG
- M4A
- FLAC
- WebM

## Project Structure

```
gke-hack/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (create this)
├── .gitignore                # Git ignore file
├── README.md                 # This file
├── services/                 # Service modules
│   ├── voice_recognition.py  # Speech-to-text service
│   ├── gemini_service.py     # Gemini AI integration
│   └── text_to_speech.py     # Text-to-speech service
├── static/                   # Static files
│   └── audio/               # Generated audio responses
└── uploads/                 # Temporary uploaded files
```

## Features in Detail

### Voice Recognition
- Uses Google Speech Recognition API
- Automatic audio format conversion
- Ambient noise adjustment
- Multi-language support

### Gemini Integration
- Uses Gemini-2.5-Flash model
- Contextual conversation support
- Specialized navigation commands
- Error handling and fallbacks

### Text-to-Speech
- Google TTS (gTTS) for high-quality speech
- Alternative pyttsx3 for offline operation
- Multiple language support
- Automatic file cleanup

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Testing the API
Use the provided test scripts or tools like Postman to test the endpoints.

### Adding New Features
1. Create new service modules in the `services/` directory
2. Import and initialize in `app.py`
3. Add new endpoints as needed
4. Update documentation

## Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Activate virtual environment

2. **Audio format not supported**
   - Convert audio to WAV format
   - Install ffmpeg for better format support

3. **Speech recognition fails**
   - Check internet connection
   - Ensure audio quality is good
   - Try shorter audio clips

4. **Gemini API errors**
   - Verify Google API key is correct
   - Check API quotas and billing
   - Ensure API is enabled in Google Cloud Console

### Logs
The application logs important events and errors. Check console output for debugging information.

## Security Notes

- Keep your Google API key secure and never commit it to version control
- Use HTTPS in production
- Implement rate limiting for production use
- Validate and sanitize all inputs
- Regularly update dependencies

## License

This project is open source. Please check the license file for more details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue in the repository

---

Made with ❤️ for voice-enabled applications