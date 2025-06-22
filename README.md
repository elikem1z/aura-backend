# 🔮 Aura: Conversational Vision Assistant Backend

A FastAPI backend for a conversational vision assistant designed to help visually impaired individuals using Meta Quest 3S. This backend integrates Vapi for voice conversations and Google Gemini for image analysis.

## 🎯 Project Overview

**Aura** is a hackathon project that provides real-time, conversational AI assistance for visually impaired users. When users ask about their surroundings, the system captures an image, analyzes it with AI, and provides detailed audio descriptions.

### Architecture Flow
```
User (Quest) → Vapi → Backend → Gemini → Backend → Vapi → User (Quest)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Vapi API key
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd aura-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   VAPI_API_KEY=your_vapi_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Test the web interface**
   Visit: http://127.0.0.1:8000/

## 📁 Project Structure

```
aura-backend/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── static/
│   └── index.html         # Web interface
├── test_*.py              # Test scripts
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Web interface for testing
- `GET /ping` - Health check
- `GET /api-info` - API information

### Image Processing
- `POST /upload-image` - Upload image from Quest app
- `POST /analyze-image` - Analyze image with Gemini AI
- `GET /image/{image_id}` - Get image information

### Vapi Integration
- `POST /webhook/vapi` - Receive function calls from Vapi

## 🧪 Testing

### Automated Tests
Run the comprehensive test suite:
```bash
python test_full_flow.py
```

### Individual Tests
- `python test_vapi.py` - Test Vapi SDK connection
- `python test_vapi_api.py` - Test Vapi API calls
- `python test_gemini.py` - Test Gemini API connection

### Web Interface Testing
1. Visit http://127.0.0.1:8000/
2. Upload an image
3. Ask a question
4. See the AI analysis result

## 🔗 Integration Guide

### For Quest App Integration

Your Quest app should:

1. **Upload Images**
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

2. **Analyze Images**
   ```javascript
   const response = await fetch('http://your-backend/analyze-image', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       image_id: imageId,
       query: userQuery
     })
   });
   ```

### For Vapi Integration

Configure Vapi webhook to point to:
```
http://your-backend/webhook/vapi
```

## 🛠️ Development

### Adding New Features
1. Create feature branch
2. Implement changes
3. Test with `test_full_flow.py`
4. Update documentation
5. Submit pull request

### Environment Setup
- **Development**: `uvicorn main:app --reload`
- **Production**: `uvicorn main:app --host 0.0.0.0 --port 8000`

## 📊 Current Status

✅ **Completed Features:**
- FastAPI backend with all endpoints
- Vapi SDK integration and testing
- Google Gemini image analysis
- Web interface for testing
- Comprehensive test suite
- Image upload and storage
- Error handling and fallbacks

🔄 **In Progress:**
- Quest app integration (partner's work)
- Vapi webhook configuration

## 🤝 Team Collaboration

### Backend Developer (You)
- Maintain and enhance the FastAPI backend
- Monitor API performance and errors
- Add new AI analysis features

### Quest App Developer (Partner)
- Integrate with backend API endpoints
- Handle image capture and upload
- Implement user interface and voice feedback

## 🚨 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
# Make sure you're in the virtual environment
venv\Scripts\activate
pip install -r requirements.txt
```

**API key errors**
- Check your `.env` file exists
- Verify API keys are correct
- Test individual APIs with test scripts

**Image analysis fails**
- Check Gemini API quota
- Verify image format (JPEG/PNG)
- Check network connectivity

### Getting Help
1. Check the logs in your terminal
2. Run individual test scripts
3. Check API documentation
4. Review error messages in web interface

## 📈 Next Steps

1. **Deploy to production server**
2. **Set up monitoring and logging**
3. **Add user authentication**
4. **Implement image storage to database**
5. **Add rate limiting and security**
6. **Optimize for performance**

## 🏆 Hackathon Goals

- [x] Backend API development
- [x] AI integration (Gemini)
- [x] Voice integration (Vapi)
- [x] Web testing interface
- [ ] Quest app integration
- [ ] End-to-end demo
- [ ] Presentation preparation


