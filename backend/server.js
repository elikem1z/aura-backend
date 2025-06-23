const express = require('express');
const cors = require('cors');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8001';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend/build')));

// Proxy API calls to Python backend
app.use('/api', createProxyMiddleware({
  target: PYTHON_API_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', // Remove /api prefix when forwarding to Python backend
  },
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying ${req.method} ${req.path} to Python backend`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Received response from Python backend: ${proxyRes.statusCode}`);
  },
}));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    backend: 'Node.js',
    python_api: PYTHON_API_URL
  });
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build/index.html'));
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Node.js server running on port ${PORT}`);
  console.log(`Proxying API calls to: ${PYTHON_API_URL}`);
  console.log(`Frontend will be available at: http://localhost:${PORT}`);
}); 