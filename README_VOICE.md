# 🎤 Aura Voice-First Vision Assistant

A revolutionary voice-powered image analysis system designed for visually impaired users. Instead of typing questions, users can speak naturally about images, and receive spoken responses through Vapi's advanced voice technology.

## 🚀 Smart Architecture

### Core Components

1. **🎙️ Voice Input via Vapi** - Users speak questions about images naturally
2. **🤖 Image Analysis via Gemini** - AI analyzes uploaded images with voice-optimized responses
3. **🔊 Voice Output via Vapi TTS** - Results spoken back to user with natural voice
4. **📱 Smart Session Management** - Track user sessions and images across interactions
5. **⚡ Real-time Processing** - Handle voice queries seamlessly

### Architecture Flow

```
User Voice → Vapi → Backend → Gemini Analysis → Voice Response → User
    ↓           ↓        ↓           ↓              ↓
  "What do   Vapi    Session    Image        "I can see a
   you see   STT     Mgmt       Analysis     red car..."
   in this
   image?"
```

## 🛠️ Setup Instructions

### 1. Environment Setup

Create a `.env` file with your API keys:

```env
# Vapi API Key - Get from https://vapi.ai/
VAPI_API_KEY=your_vapi_api_key_here

# Google Gemini API Key - Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Voice-First Server

```bash
# Start the voice-first server
python -m uvicorn main_voice:app --reload --host 127.0.0.1 --port 8000
```

### 4. Test the Voice Architecture

```bash
# Run comprehensive voice-first tests
python test_voice_flow.py
```

## 📡 API Endpoints

### Voice-First Endpoints

#### Create Voice Session
```http
POST /voice/session/create
Content-Type: application/x-www-form-urlencoded

user_id=your_user_id
```

**Response:**
```json
{
  "session_id": "uuid-session-id",
  "message": "Voice session created successfully",
  "voice_enabled": true
}
```

#### Process Voice Query
```http
POST /voice/query
Content-Type: application/json

{
  "session_id": "uuid-session-id",
  "query": "What do you see in this image?",
  "image_id": "optional-specific-image-id"
}
```

**Response:**
```json
{
  "response": "I can see a red car parked in front of a building...",
  "audio_url": "/static/audio/uuid-audio.mp3",
  "session_id": "uuid-session-id"
}
```

#### Get Voice Session Info
```http
GET /voice/session/{session_id}
```

**Response:**
```json
{
  "session_id": "uuid-session-id",
  "user_id": "user123",
  "created_at": "2024-01-01T12:00:00",
  "last_activity": "2024-01-01T12:05:00",
  "images": ["image1", "image2"],
  "current_image": "image2",
  "voice_enabled": true
}
```

### Image Management

#### Upload Image (Voice-Enhanced)
```http
POST /upload-image
Content-Type: multipart/form-data

image: [file]
user_id: your_user_id
session_id: uuid-session-id (optional)
```

#### Analyze Image (with Voice Output)
```http
POST /analyze-image
Content-Type: application/json

{
  "image_id": "uuid-image-id",
  "query": "What colors do you see?",
  "session_id": "uuid-session-id"
}
```

### Vapi Webhook

#### Handle Vapi Function Calls
```http
POST /webhook/vapi
Content-Type: application/json

{
  "message": {
    "type": "function-call",
    "functionCall": {
      "name": "describeSurroundings",
      "arguments": {
        "session_id": "uuid-session-id",
        "query": "What do you see?"
      }
    }
  }
}
```

## 🎯 Vapi Integration

### 1. Configure Vapi Assistant

Use the provided `vapi_config.json` to set up your Vapi assistant:

```json
{
  "name": "Aura Vision Assistant",
  "description": "Voice-powered image analysis assistant",
  "model": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "systemPrompt": "You are Aura, a helpful vision assistant...",
    "functions": [
      {
        "name": "describeSurroundings",
        "description": "Analyze an image and describe what the user is looking at"
      },
      {
        "name": "uploadImage", 
        "description": "Upload a new image for analysis"
      }
    ]
  },
  "webhook": {
    "url": "http://your-backend-url/webhook/vapi"
  }
}
```

### 2. Voice Assistant Features

- **Natural Voice Input**: Users speak questions naturally
- **Intelligent Responses**: Context-aware image analysis
- **Voice Output**: Natural-sounding responses via TTS
- **Session Continuity**: Remember user context across interactions
- **Interruption Support**: Users can interrupt and ask follow-up questions

## 🔧 Development

### Project Structure

```
aura-backend/
├── main_voice.py              # Voice-first FastAPI application
├── voice_manager.py           # Vapi voice integration
├── session_manager.py         # Session management
├── vapi_config.json          # Vapi assistant configuration
├── test_voice_flow.py        # Voice architecture tests
├── static/
│   ├── index.html            # Enhanced web interface
│   └── audio/                # Generated audio files
├── requirements.txt          # Python dependencies
└── README_VOICE.md          # This file
```

### Key Features

#### Voice Manager (`voice_manager.py`)
- Text-to-Speech via Vapi
- Voice query processing
- Audio file management

#### Session Manager (`session_manager.py`)
- User session tracking
- Image association
- Voice session state

#### Voice-First API (`main_voice.py`)
- Voice-optimized endpoints
- Real-time processing
- Webhook integration

## 🧪 Testing

### Run Voice Architecture Tests

```bash
# Test the complete voice-first flow
python test_voice_flow.py
```

This will test:
1. ✅ Server health check
2. ✅ Voice session creation
3. ✅ Image upload
4. ✅ Voice query processing
5. ✅ Image analysis with voice output
6. ✅ Session management
7. ✅ Vapi webhook functionality

### Manual Testing

1. **Create Voice Session:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/voice/session/create" \
        -d "user_id=test_user"
   ```

2. **Upload Image:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/upload-image" \
        -F "image=@test_image.jpg" \
        -F "user_id=test_user" \
        -F "session_id=your_session_id"
   ```

3. **Process Voice Query:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/voice/query" \
        -H "Content-Type: application/json" \
        -d '{"session_id":"your_session_id","query":"What do you see?"}'
   ```

## 🌐 Web Interface

Visit `http://127.0.0.1:8000/` for the enhanced web interface with:

- 🎙️ Voice session creation
- 📸 Image upload with voice support
- 🔍 Voice query processing
- 🔊 Audio playback of responses

## 🔗 Integration Guide

### For Quest App Integration

Your Quest app should:

1. **Create Voice Session:**
   ```javascript
   const response = await fetch('http://your-backend/voice/session/create', {
     method: 'POST',
     body: new FormData([['user_id', userId]])
   });
   const { session_id } = await response.json();
   ```

2. **Upload Images:**
   ```javascript
   const formData = new FormData();
   formData.append('image', imageFile);
   formData.append('user_id', userId);
   formData.append('session_id', sessionId);
   
   const response = await fetch('http://your-backend/upload-image', {
     method: 'POST',
     body: formData
   });
   ```

3. **Process Voice Queries:**
   ```javascript
   const response = await fetch('http://your-backend/voice/query', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       session_id: sessionId,
       query: voiceQuery
     })
   });
   const { response: textResponse, audio_url } = await response.json();
   ```

### For Vapi Integration

1. **Configure Vapi Assistant** using `vapi_config.json`
2. **Set Webhook URL** to `http://your-backend/webhook/vapi`
3. **Deploy Assistant** to Vapi platform
4. **Test Voice Interactions** through Vapi interface

## 🚀 Deployment

### Production Setup

1. **Environment Variables:**
   ```bash
   export VAPI_API_KEY="your_vapi_key"
   export GEMINI_API_KEY="your_gemini_key"
   ```

2. **Start Production Server:**
   ```bash
   uvicorn main_voice:app --host 0.0.0.0 --port 8000
   ```

3. **Configure Vapi Webhook:**
   - Update `vapi_config.json` with your production URL
   - Deploy assistant to Vapi

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main_voice:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Performance

### Voice Optimization

- **Response Length**: Optimized for voice (1024 tokens max)
- **Audio Quality**: High-quality TTS via Vapi
- **Session Caching**: Efficient session management
- **Real-time Processing**: Sub-second response times

### Scalability

- **Session Management**: In-memory with cleanup
- **Image Storage**: Efficient binary storage
- **Voice Processing**: Async TTS generation
- **Webhook Handling**: Stateless function calls

## 🔒 Security

- **API Key Protection**: Environment variable storage
- **Session Isolation**: User session separation
- **Input Validation**: File type and size validation
- **Error Handling**: Graceful fallbacks

## 🎯 Use Cases

### Primary Use Cases

1. **Visually Impaired Assistance**: Help users understand their surroundings
2. **Accessibility**: Voice-first interaction for better accessibility
3. **Hands-free Operation**: Voice commands for hands-free use
4. **Natural Interaction**: Conversational image analysis

### Example Interactions

**User:** "What do you see in this image?"
**Aura:** "I can see a red car parked in front of a modern office building. The car appears to be a sedan with tinted windows..."

**User:** "Are there any people in the image?"
**Aura:** "No, I don't see any people in this image. The scene shows just the car and the building..."

## 🚀 Future Enhancements

- **Multi-language Support**: Voice in different languages
- **Real-time Video**: Live video analysis
- **Voice Biometrics**: User voice recognition
- **Advanced AI**: More sophisticated image understanding
- **Mobile App**: Native mobile voice interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement voice-first enhancements
4. Test with `test_voice_flow.py`
5. Submit pull request

## 📞 Support

For questions about the voice-first architecture:
- Check the test results
- Review the API documentation
- Test with the web interface
- Check server logs for errors

---

**🎤 Transform your vision assistant into a voice-first experience with Aura!** 