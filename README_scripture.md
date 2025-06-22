# Scripture Finder

A modern, AI-powered Bible search application with voice recognition and intelligent analysis.

## 🚀 Current Status

The app is **fully functional** for basic Bible searches! However, for the full AI-powered experience, you need to add a Gemini API key.

### ✅ What Works Now
- Bible verse searches using multiple APIs
- Beautiful yellow-themed UI with interactive effects
- Voice recognition (microphone input)
- Text-to-speech capabilities
- Modern responsive design
- Ready for deployment on Render.com with HTTPS

### 🔧 What Needs Setup
- **Gemini API Key** for intelligent AI analysis and explanations

## 🎯 Quick Setup

### Option 1: Run Setup Script (Recommended)
```bash
cd backend
python setup.py
```

### Option 2: Manual Setup
1. Get a free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the `backend` folder:
```env
BIBLE_API_KEY=a1692756d99fab00256e70dbda406cc7
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

## 🏃‍♂️ Running the App

```bash
cd backend
python app.py
```

Open http://localhost:5000 in your browser.

## 🌟 Features

### Current Features
- **Bible Search**: Search verses using natural language
- **Voice Input**: Speak your questions using microphone
- **Multiple APIs**: Uses both Biblia.com and Bible-API.com
- **Modern UI**: Beautiful yellow gradient theme with animations
- **Responsive Design**: Works on desktop and mobile
- **Text-to-Speech**: Hear responses aloud

### With Gemini AI (After Setup)
- **Intelligent Analysis**: AI-powered explanations of verses
- **Query Refinement**: Automatically improves search terms
- **Context Understanding**: Better understanding of natural language
- **Confidence Scoring**: Shows how confident the AI is in results

## 🎨 UI Features

- **Interactive Cursor**: Follows your mouse with smooth animations
- **Floating Particles**: Ambient background effects
- **Hover Animations**: Cards lift and glow on hover
- **Ripple Effects**: Button click animations
- **Yellow Theme**: Beautiful gradient design
- **Voice Recognition**: Real-time speech input

## 🚀 Deployment with HTTPS (Free)

### Render.com (Recommended - Free HTTPS)
1. **Push to GitHub**: Upload your code to GitHub
2. **Connect to Render**: Go to [render.com](https://render.com), connect your GitHub repository
3. **Deploy**: Render will automatically deploy with HTTPS
4. **Set Environment Variables**:
   - `GEMINI_API_KEY`: Your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `BIBLE_API_KEY`: Bible API key (already included)
5. **Test Microphone**: Your app will have HTTPS and full features!

### Other Free HTTPS Options
- **Railway**: Direct deployment from GitHub with HTTPS
- **Vercel**: Python runtime support with HTTPS
- **Netlify**: Static site hosting with HTTPS

## 📁 Project Structure

```
SystemTracker/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── templates/
│   │   └── index.html      # Frontend interface
│   ├── requirements.txt    # Python dependencies
│   ├── setup.py           # Setup script
│   ├── .env               # Environment variables
│   ├── Procfile           # Heroku deployment
│   └── runtime.txt        # Python version
├── frontend/              # Legacy frontend (not used)
├── render.yaml            # Render deployment config
└── README.md
```

## 🔧 Technical Details

### Backend (Flask)
- **Flask**: Web framework
- **Google Generative AI**: For intelligent analysis
- **Bible APIs**: Multiple sources for comprehensive results
- **gTTS**: Text-to-speech conversion
- **CORS**: Cross-origin support

### Frontend (HTML/CSS/JS)
- **Vanilla JavaScript**: No frameworks needed
- **Web Speech API**: Voice recognition
- **CSS Animations**: Smooth interactions
- **Responsive Design**: Mobile-friendly

## 🎯 Usage Examples

### Basic Searches (Works Now)
- "John 3:16"
- "love"
- "Matthew 24"
- "golden lampstands"

### AI-Enhanced (After Gemini Setup)
- "What does the Bible say about forgiveness?"
- "I'm feeling anxious, show me comforting verses"
- "Explain the parable of the prodigal son"
- "What are the fruits of the Spirit?"

## 🛠️ Troubleshooting

### Common Issues

1. **"AI analysis not available"**
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add it to your `.env` file

2. **Microphone not working**
   - Ensure you're on HTTPS (required for microphone access)
   - Check browser permissions
   - Try refreshing the page

3. **Deployment issues on Render**
   - Set environment variables in Render dashboard
   - Ensure build command is: `pip install -r backend/requirements.txt`
   - Start command should be: `cd backend && python app.py`

### Getting Help
- Check the browser console for errors
- Verify your API keys are correct
- Ensure all dependencies are installed

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Bible APIs for providing scripture data
- Google AI for Gemini capabilities
- Web Speech API for voice recognition
- Flask community for the excellent framework

---

**Ready to explore the Bible with AI? Get your Gemini API key and start searching! 🚀**