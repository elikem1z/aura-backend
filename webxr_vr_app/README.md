# 🎮 Aura VR - WebXR Voice-First Image Analysis

A lightweight WebXR application that connects to your FastAPI backend for real-time voice-first image analysis in VR.

## 🚀 Features

- **WebXR Support**: Works on Meta Quest, PC VR, and mobile VR
- **Voice Recognition**: Built-in speech-to-text for natural queries
- **Screenshot Capture**: Capture VR views and analyze them with AI
- **Real-time Audio**: Get AI responses as audio in your VR headset
- **Lightweight**: No heavy Unity/Unreal installations required
- **Cross-platform**: Works on any WebXR-compatible device

## 📋 Prerequisites

- **Meta Quest** (or any WebXR-compatible VR headset)
- **FastAPI Backend** running on port 8001 (your existing Aura backend)
- **Python 3.7+** (for the web server)
- **Modern Web Browser** with WebXR support

## 🛠️ Installation & Setup

### 1. Start Your FastAPI Backend

First, make sure your Aura backend is running:

```bash
# In your aura-backend directory
python -m uvicorn main_voice:app --reload --port 8001
```

### 2. Start the WebXR Server

```bash
# In the webxr_vr_app directory
python server.py
```

The server will start on `http://localhost:8080`

### 3. Access from Meta Quest

#### Option A: Same Network (Recommended)
1. Find your computer's IP address:
   ```bash
   # On Windows
   ipconfig
   
   # On Mac/Linux
   ifconfig
   ```

2. On your Meta Quest:
   - Open the browser
   - Navigate to: `http://YOUR_COMPUTER_IP:8080`
   - Example: `http://192.168.1.100:8080`

#### Option B: Local Development
- Use `http://localhost:8080` if testing on the same device

## 🎮 How to Use

### 1. Enter VR Mode
- Click the "Enter VR" button in the browser
- Put on your VR headset
- Use VR controllers to navigate

### 2. Connect to Backend
- Click "Connect to Backend" to establish connection
- Wait for the green "Connected" status

### 3. Capture Screenshots
- Click "Capture Screenshot" to take a photo of your VR view
- The image is automatically uploaded to your FastAPI backend

### 4. Analyze Images
- **Auto Analysis**: Click "Analyze Image" for automatic description
- **Voice Query**: Click "Voice Query" and speak your question
- Listen to the AI's audio response in your VR headset

### 5. Voice Commands
- "What do you see in this image?"
- "Describe the objects in front of me"
- "What colors are visible?"
- "Is there any text in the image?"

## 🔧 Configuration

### Backend URL
Edit `app.js` to change the backend URL:
```javascript
this.backendUrl = 'http://YOUR_BACKEND_IP:8001';
```

### Port Configuration
Edit `server.py` to change the web server port:
```python
PORT = 8080  # Change this if needed
```

## 📁 File Structure

```
webxr_vr_app/
├── index.html          # Main HTML file
├── app.js             # WebXR application logic
├── server.py          # Simple HTTP server
└── README.md          # This file
```

## 🎯 Technical Details

### WebXR Features
- **Three.js**: 3D graphics and WebXR support
- **VR Controllers**: Full controller support for Meta Quest
- **Screenshot Capture**: Canvas-based image capture
- **Audio Playback**: Direct audio streaming from backend

### Backend Integration
- **REST API**: Communicates with your FastAPI backend
- **Session Management**: Maintains VR user sessions
- **File Upload**: Sends screenshots for analysis
- **Audio Streaming**: Receives and plays TTS responses

### Voice Recognition
- **Web Speech API**: Built-in browser speech recognition
- **Real-time Processing**: Immediate voice-to-text conversion
- **Error Handling**: Graceful fallback for unsupported browsers

## 🐛 Troubleshooting

### Connection Issues
1. **Backend not responding**: Ensure FastAPI is running on port 8001
2. **CORS errors**: The server includes CORS headers, but check your backend
3. **Network issues**: Make sure Quest and computer are on same network

### VR Issues
1. **WebXR not supported**: Update your browser or use a different one
2. **Controllers not working**: Try refreshing the page
3. **Performance issues**: Close other VR applications

### Voice Recognition Issues
1. **Microphone access**: Allow microphone permissions in browser
2. **No speech detected**: Check microphone settings in Quest
3. **Language issues**: Currently supports English only

## 🔒 Security Notes

- This is a development setup with CORS enabled for all origins
- For production, configure proper CORS settings
- Consider HTTPS for secure connections
- Implement proper authentication if needed

## 🚀 Production Deployment

For production use:

1. **HTTPS Setup**: Configure SSL certificates
2. **CORS Configuration**: Restrict origins to your domain
3. **Authentication**: Add user authentication
4. **CDN**: Use a CDN for better performance
5. **Monitoring**: Add logging and monitoring

## 📞 Support

If you encounter issues:

1. Check the browser console for error messages
2. Verify your FastAPI backend is running and accessible
3. Test the backend endpoints directly
4. Check network connectivity between Quest and computer

## 🎉 Success!

You now have a complete VR voice-first image analysis system! 

- **Lightweight**: No heavy game engines required
- **Real-time**: Instant voice queries and responses
- **Accessible**: Works with any WebXR-compatible device
- **Extensible**: Easy to modify and enhance

Enjoy your AI-powered VR assistant! 🎮🤖 