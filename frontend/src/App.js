import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, Mic, MicOff, Send, Image, Volume2, VolumeX } from 'lucide-react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageId, setImageId] = useState(null);
  const [query, setQuery] = useState('');
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const fileInputRef = useRef(null);
  const audioRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setUploadStatus('');
      setAnalysisResult(null);
      setAudioUrl(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select an image first');
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading image...');

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('/api/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setImageId(response.data.image_id);
      setUploadStatus('Image uploaded successfully! Ready to analyze.');
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!imageId) {
      setAnalysisResult('Please upload an image first');
      return;
    }

    if (!query.trim()) {
      setAnalysisResult('Please enter a question about the image');
      return;
    }

    setIsAnalyzing(true);
    setAnalysisResult('Analyzing image...');

    try {
      const response = await axios.post('/api/analyze-image', {
        image_id: imageId,
        query: query.trim(),
        voice_response: voiceEnabled,
      });

      setAnalysisResult(response.data.description);
      
      if (voiceEnabled && response.data.audio_url) {
        setAudioUrl(response.data.audio_url);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      setAnalysisResult('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleAnalyze();
    }
  };

  const playAudio = () => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Aura Vision Assistant
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered image analysis with voice capabilities
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Image className="w-5 h-5 mr-2" />
              Upload Image
            </h2>
            
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileSelect}
                  accept="image/*"
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex flex-col items-center space-y-2 text-gray-600 hover:text-primary-600"
                >
                  <Upload className="w-8 h-8" />
                  <span className="font-medium">
                    {selectedFile ? selectedFile.name : 'Click to select image'}
                  </span>
                </button>
              </div>

              {selectedFile && (
                <div className="text-sm text-gray-600">
                  Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!selectedFile || isUploading}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isUploading ? 'Uploading...' : 'Upload Image'}
              </button>

              {uploadStatus && (
                <div className={`text-sm p-3 rounded-lg ${
                  uploadStatus.includes('successfully') 
                    ? 'bg-green-50 text-green-700 border border-green-200' 
                    : uploadStatus.includes('failed') 
                    ? 'bg-red-50 text-red-700 border border-red-200'
                    : 'bg-blue-50 text-blue-700 border border-blue-200'
                }`}>
                  {uploadStatus}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Analysis */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Mic className="w-5 h-5 mr-2" />
              Analyze Image
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Question about the image
                </label>
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about the image..."
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
              </div>

              <div className="flex items-center space-x-3">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={voiceEnabled}
                    onChange={(e) => setVoiceEnabled(e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Voice Response</span>
                </label>
                {voiceEnabled ? (
                  <Volume2 className="w-4 h-4 text-green-600" />
                ) : (
                  <VolumeX className="w-4 h-4 text-gray-400" />
                )}
              </div>

              <button
                onClick={handleAnalyze}
                disabled={!imageId || !query.trim() || isAnalyzing}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
              >
                <Send className="w-4 h-4" />
                <span>{isAnalyzing ? 'Analyzing...' : 'Analyze Image'}</span>
              </button>

              {analysisResult && (
                <div className="space-y-3">
                  <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <h3 className="font-medium text-gray-900 mb-2">Analysis Result</h3>
                    <p className="text-gray-700">{analysisResult}</p>
                  </div>

                  {audioUrl && voiceEnabled && (
                    <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Volume2 className="w-4 h-4 text-green-600" />
                          <span className="text-sm font-medium text-green-800">Voice Response Available</span>
                        </div>
                        <button
                          onClick={playAudio}
                          className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                        >
                          Play Audio
                        </button>
                      </div>
                      <audio ref={audioRef} src={audioUrl} className="hidden" />
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500">
          <p>Powered by Google Gemini AI and Google Cloud TTS</p>
        </div>
      </div>
    </div>
  );
}

export default App; 