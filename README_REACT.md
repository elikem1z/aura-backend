# Aura Vision Assistant - React Frontend

A modern, professional React frontend for the Aura Vision Assistant with Node.js backend proxy.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- Python 3.8+ (for the AI backend)
- npm or yarn

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 2. Install Backend Dependencies
```bash
cd backend
npm install
```

### 3. Start the Python AI Backend
```bash
# In the root directory
uvicorn main_voice_simple:app --reload --port 8001
```

### 4. Build and Start the React Frontend
```bash
# Build the React app
cd frontend
npm run build

# Start the Node.js server (serves React app + proxies to Python)
cd ../backend
npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Python API**: http://localhost:8001
- **Health Check**: http://localhost:3000/health

## 📁 Project Structure

```
aura-backend/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Tailwind CSS styles
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── package.json         # Frontend dependencies
│   └── tailwind.config.js   # Tailwind configuration
├── backend/                  # Node.js proxy server
│   ├── server.js            # Express server
│   └── package.json         # Backend dependencies
├── main_voice_simple.py     # Python AI backend
├── voice_manager.py         # Voice/TTS functionality
└── requirements.txt         # Python dependencies
```

## 🎨 Features

### Modern UI/UX
- **Professional Design**: Clean, modern interface without emojis
- **Responsive Layout**: Works on desktop and mobile
- **Tailwind CSS**: Modern styling framework
- **Lucide Icons**: Professional icon set
- **Smooth Animations**: Hover effects and transitions

### User Experience
- **Drag & Drop**: Easy image upload
- **Real-time Feedback**: Loading states and status messages
- **Voice Toggle**: Enable/disable voice responses
- **Audio Player**: Built-in audio playback
- **Error Handling**: User-friendly error messages

### Technical Features
- **React 18**: Modern React with hooks
- **Axios**: HTTP client for API calls
- **Node.js Proxy**: Seamless API routing
- **CORS Support**: Cross-origin requests
- **Environment Variables**: Configurable settings

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm start          # Start React dev server
npm run build      # Build for production
npm test           # Run tests
```

### Backend Development
```bash
cd backend
npm run dev        # Start with nodemon (auto-restart)
npm start          # Start production server
```

### Environment Variables
```bash
# Backend (.env)
PORT=3000
PYTHON_API_URL=http://localhost:8001

# Frontend (.env)
REACT_APP_API_URL=http://localhost:3000/api
```

## 🚀 Deployment

### Production Build
```bash
# Build React app
cd frontend
npm run build

# Start production server
cd ../backend
npm start
```

### Docker Deployment
```dockerfile
# Dockerfile for Node.js backend
FROM node:16-alpine
WORKDIR /app
COPY backend/package*.json ./
RUN npm install
COPY backend/ ./
COPY frontend/build ./frontend/build
EXPOSE 3000
CMD ["npm", "start"]
```

### Platform Deployment
- **Render**: Use the Node.js backend as the main service
- **Railway**: Deploy both frontend and backend
- **Heroku**: Use the Node.js backend with buildpacks

## 🔌 API Integration

The Node.js backend proxies all API calls to the Python backend:

- `/api/upload-image` → `http://localhost:8001/upload-image`
- `/api/analyze-image` → `http://localhost:8001/analyze-image`
- `/api/voice/query` → `http://localhost:8001/voice/query`

## 🎯 Key Improvements

### Over Previous Version
- **No Emojis**: Professional, clean interface
- **Modern Stack**: React + Node.js + Tailwind CSS
- **Better UX**: Improved loading states and feedback
- **Responsive**: Mobile-friendly design
- **Maintainable**: Separated frontend and backend concerns
- **Scalable**: Easy to extend and modify

### Technical Benefits
- **Type Safety**: Ready for TypeScript migration
- **Component Reusability**: Modular React components
- **Performance**: Optimized builds and caching
- **SEO Friendly**: Server-side rendering ready
- **Testing**: Jest and React Testing Library setup

## 🛠️ Customization

### Styling
- Modify `frontend/tailwind.config.js` for theme changes
- Update `frontend/src/index.css` for global styles
- Use Tailwind utility classes in components

### Components
- Add new components in `frontend/src/components/`
- Update `App.js` for layout changes
- Extend functionality with additional React hooks

### API Integration
- Modify `backend/server.js` for additional proxy routes
- Update API calls in `frontend/src/App.js`
- Add new endpoints as needed

## 📝 License

MIT License - see LICENSE file for details. 