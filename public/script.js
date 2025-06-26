// Interactive Network Background Animation
class NetworkBackground {
    constructor() {
        this.canvas = document.getElementById('network-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null };
        this.animationId = null;
        
        this.init();
        this.setupEventListeners();
        this.animate();
    }
    
    init() {
        this.resizeCanvas();
        this.createParticles();
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        const numberOfParticles = Math.min(Math.floor((this.canvas.width * this.canvas.height) / 10000), 150);
        this.particles = [];
        
        for (let i = 0; i < numberOfParticles; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createParticles();
        });
        
        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
        
        document.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }
    
    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(96, 165, 250, ${particle.opacity})`;
        this.ctx.fill();
    }
    
    drawConnection(particle1, particle2, distance, maxDistance) {
        const opacity = (1 - distance / maxDistance) * 0.3;
        this.ctx.beginPath();
        this.ctx.moveTo(particle1.x, particle1.y);
        this.ctx.lineTo(particle2.x, particle2.y);
        this.ctx.strokeStyle = `rgba(96, 165, 250, ${opacity})`;
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
    
    drawMouseConnections(particle) {
        if (this.mouse.x === null || this.mouse.y === null) return;
        
        const dx = this.mouse.x - particle.x;
        const dy = this.mouse.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxDistance = 150;
        
        if (distance < maxDistance) {
            const opacity = (1 - distance / maxDistance) * 0.8;
            this.ctx.beginPath();
            this.ctx.moveTo(particle.x, particle.y);
            this.ctx.lineTo(this.mouse.x, this.mouse.y);
            this.ctx.strokeStyle = `rgba(96, 165, 250, ${opacity})`;
            this.ctx.lineWidth = 2;
            this.ctx.stroke();
            
            // Mouse attraction effect
            const force = (maxDistance - distance) / maxDistance;
            particle.vx += dx * force * 0.00005;
            particle.vy += dy * force * 0.00005;
        }
    }
    
    updateParticle(particle) {
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        // Boundary collision
        if (particle.x <= 0 || particle.x >= this.canvas.width) {
            particle.vx *= -1;
            particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
        }
        if (particle.y <= 0 || particle.y >= this.canvas.height) {
            particle.vy *= -1;
            particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
        }
        
        // Damping
        particle.vx *= 0.999;
        particle.vy *= 0.999;
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw particles
        this.particles.forEach(particle => {
            this.updateParticle(particle);
            this.drawParticle(particle);
            this.drawMouseConnections(particle);
        });
        
        // Draw connections between particles
        const maxConnectionDistance = 120;
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < maxConnectionDistance) {
                    this.drawConnection(this.particles[i], this.particles[j], distance, maxConnectionDistance);
                }
            }
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Advanced AURA Vision App with Conversational AI
class AuraVisionApp {
    constructor() {
        this.selectedFile = null;
        this.imageId = null;
        this.sessionId = null;
        this.voiceEnabled = true;
        this.voiceInputEnabled = true;
        this.audioElement = null;
        this.recognition = null;
        this.wakeWordRecognition = null;
        this.isListening = false;
        this.isWakeWordListening = false;
        this.isProcessing = false;
        this.isSpeaking = false;
        this.availableModels = [];
        this.selectedModel = 'gemini-1.5-flash';
        
        this.initializeElements();
        this.setupEventListeners();
        this.initializeSession();
        this.loadAvailableModels();
        this.updateDashboard();
        this.setupVoiceRecognition();
        this.setupWakeWordDetection();
        
        // Auto-refresh stats every 30 seconds
        setInterval(() => this.updateDashboard(), 30000);
    }
    
    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.imageInput = document.getElementById('imageInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.uploadStatus = document.getElementById('uploadStatus');
        
        // Analysis elements (voice-only interface)
        this.queryInput = document.getElementById('queryInput'); // Hidden, for voice-to-text only
        this.modelSelect = document.getElementById('modelSelect');
        this.modelInfo = document.getElementById('modelInfo');
        this.voiceToggle = document.getElementById('voiceToggle');
        this.voiceInputToggle = document.getElementById('voiceInputToggle');
        this.stopBtn = document.getElementById('stopBtn');
        this.analysisResult = document.getElementById('analysisResult');
        
        // Status elements
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.querySelector('.status-text');
        
        // Dashboard elements
        this.globalImagesEl = document.getElementById('globalImagesProcessed');
        this.totalAnalysesEl = document.getElementById('totalAnalyses');
        this.activeSessionsEl = document.getElementById('activeSessions');
        this.currentModelEl = document.getElementById('currentModel');
    }
    
    async initializeSession() {
        try {
            const response = await fetch('/api/session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'create' })
            });
            const result = await response.json();
            this.sessionId = result.session_id;
            console.log('Session initialized:', this.sessionId);
        } catch (error) {
            console.error('Failed to initialize session:', error);
        }
    }
    
    async loadAvailableModels() {
        try {
            const response = await fetch('/api/models');
            const result = await response.json();
            this.availableModels = result.models;
            
            // Update model selector
            this.modelSelect.innerHTML = '';
            this.availableModels.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = `${model.name} - ${model.description}`;
                this.modelSelect.appendChild(option);
            });
            
            this.updateModelInfo();
        } catch (error) {
            console.error('Failed to load models:', error);
        }
    }
    
    updateModelInfo() {
        const selectedModel = this.availableModels.find(m => m.id === this.selectedModel);
        if (selectedModel) {
            this.modelInfo.innerHTML = `
                <strong>Strengths:</strong> ${selectedModel.strengths.join(', ')}<br>
                <strong>Max Tokens:</strong> ${selectedModel.maxTokens.toLocaleString()}
            `;
            
            // Update dashboard
            const modelName = selectedModel.name.split(' ').pop(); // Get last word (Flash/Pro)
            if (this.currentModelEl) {
                this.currentModelEl.textContent = modelName;
            }
        }
    }
    
    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window) {
            // Main recognition for commands
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateAssistantStatus('listening', 'AURA Listening...');
                this.stopBtn.style.display = 'block';
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript.toLowerCase().trim();
                console.log('Voice command received:', transcript);
                
                // Check if it's a wake word command
                if (this.isWakeWordCommand(transcript)) {
                    // Extract the command after wake word
                    const command = this.extractCommandFromWakeWord(transcript);
                    if (command) {
                        this.queryInput.value = command;
                        this.stopListening();
                        
                        // Auto-analyze if image is uploaded
                        if (this.imageId) {
                            setTimeout(() => this.analyzeImage(), 500);
                        } else {
                            this.showStatus('Please upload an image first before asking questions.', 'info');
                        }
                    }
                } else {
                    // Regular voice input
                    this.queryInput.value = transcript;
                    this.stopListening();
                    
                    // Auto-analyze if image is uploaded
                    if (this.imageId) {
                        setTimeout(() => this.analyzeImage(), 500);
                    }
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.stopListening();
                
                // Enhanced error handling
                switch(event.error) {
                    case 'no-speech':
                        this.showStatus('No speech detected. Please try again.', 'info');
                        break;
                    case 'audio-capture':
                        this.showStatus('Microphone access required for voice commands.', 'error');
                        break;
                    case 'not-allowed':
                        this.showStatus('Microphone permission denied.', 'error');
                        break;
                    default:
                        this.showStatus('Voice recognition error. Please try again.', 'error');
                }
            };
            
            this.recognition.onend = () => {
                this.stopListening();
            };
        } else {
            this.voiceInputToggle.style.opacity = '0.5';
            this.showStatus('Voice recognition not supported in this browser.', 'error');
        }
    }
    
    setupWakeWordDetection() {
        if ('webkitSpeechRecognition' in window) {
            // Separate recognition instance for wake word detection
            this.wakeWordRecognition = new webkitSpeechRecognition();
            this.wakeWordRecognition.continuous = true; // Keep listening continuously
            this.wakeWordRecognition.interimResults = true; // Get interim results for faster detection
            this.wakeWordRecognition.lang = 'en-US';
            
            this.wakeWordRecognition.onstart = () => {
                this.isWakeWordListening = true;
                console.log('Wake word detection started');
            };
            
            this.wakeWordRecognition.onresult = (event) => {
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript.toLowerCase().trim();
                    
                    // Check for wake words
                    if (this.containsWakeWord(transcript)) {
                        console.log('Wake word detected:', transcript);
                        
                        // Stop wake word recognition temporarily
                        this.stopWakeWordDetection();
                        
                        // Generate casual response
                        this.respondToWakeWord();
                        
                        // Start listening for command after brief delay
                        setTimeout(() => {
                            this.updateAssistantStatus('listening', 'Listening for your question...');
                            this.startListeningForCommand();
                        }, 1500); // Give time for casual response
                        
                        break;
                    }
                }
            };
            
            this.wakeWordRecognition.onerror = (event) => {
                if (event.error === 'no-speech') {
                    // This is normal for continuous listening, just restart
                    setTimeout(() => {
                        if (this.voiceInputEnabled) {
                            this.startWakeWordDetection();
                        }
                    }, 1000);
                } else {
                    console.error('Wake word recognition error:', event.error);
                    // Restart wake word detection after error
                    setTimeout(() => {
                        if (this.voiceInputEnabled) {
                            this.startWakeWordDetection();
                        }
                    }, 2000);
                }
            };
            
            this.wakeWordRecognition.onend = () => {
                this.isWakeWordListening = false;
                // Automatically restart wake word detection if voice input is enabled
                if (this.voiceInputEnabled && !this.isListening) {
                    setTimeout(() => this.startWakeWordDetection(), 1000);
                }
            };
        }
    }
    
    respondToWakeWord() {
        // Array of casual, short responses with more variety
        const casualResponses = [
            "What's up?",
            "Hey there!",
            "Yooooo!",
            "Hey!",
            "Sup?",
            "Yeah?",
            "I'm here!",
            "What's good?",
            "Yo!",
            "Hey hey!",
            "Wassup?",
            "Hi there!",
            "Yeah, what's up?",
            "I'm listening!",
            "What's on your mind?",
            "Ready when you are!",
            "Go ahead!",
            "I'm all ears!",
            "Talk to me!"
        ];
        
        // Pick a random casual response
        const response = casualResponses[Math.floor(Math.random() * casualResponses.length)];
        
        // Update status
        this.updateAssistantStatus('speaking', `AURA: "${response}"`);
        
        // Generate and play audio response if voice is enabled
        if (this.voiceEnabled) {
            this.generateAndPlayCasualResponse(response);
        }
        
        // Show the response in UI briefly
        this.showStatus(`🎤 AURA: "${response}"`, 'info');
        
        console.log('AURA casual response:', response);
    }
    
    async generateAndPlayCasualResponse(text) {
        try {
            // Strip HTML tags for clean TTS
            const cleanText = this.stripHTMLTags(text);
            
            // Use the TTS endpoint to generate audio for the casual response
            const response = await fetch('/api/generate-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: cleanText })
            });
            
            if (response.ok) {
                const result = await response.json();
                if (result.audio_url) {
                    // Play the casual response
                    this.playAudio(result.audio_url, true); // true flag for casual response
                }
            }
        } catch (error) {
            console.error('Failed to generate casual TTS response:', error);
            // If TTS fails, just continue without audio
        }
    }
    
    // Helper function to strip HTML tags
    stripHTMLTags(html) {
        if (!html) return '';
        
        return html
            .replace(/<[^>]*>/g, '') // Remove HTML tags
            .replace(/&nbsp;/g, ' ') // Replace &nbsp; with space
            .replace(/&amp;/g, '&')  // Replace &amp; with &
            .replace(/&lt;/g, '<')   // Replace &lt; with <
            .replace(/&gt;/g, '>')   // Replace &gt; with >
            .replace(/&quot;/g, '"') // Replace &quot; with "
            .replace(/&#39;/g, "'")  // Replace &#39; with '
            .replace(/\s+/g, ' ')    // Replace multiple spaces with single space
            .trim();                 // Remove leading/trailing whitespace
    }
    
    containsWakeWord(transcript) {
        const wakeWords = ['hey aura', 'aura', 'hey ara', 'ara'];
        return wakeWords.some(wakeWord => transcript.includes(wakeWord));
    }
    
    isWakeWordCommand(transcript) {
        return transcript.startsWith('hey aura') || transcript.startsWith('aura');
    }
    
    extractCommandFromWakeWord(transcript) {
        let command = transcript;
        if (command.startsWith('hey aura')) {
            command = command.substring(8).trim();
        } else if (command.startsWith('aura')) {
            command = command.substring(4).trim();
        }
        
        command = command.replace(/^(please|can you|could you|would you)\s+/i, '');
        
        return command || null;
    }
    
    startWakeWordDetection() {
        if (this.wakeWordRecognition && this.voiceInputEnabled && !this.isWakeWordListening && !this.isListening) {
            try {
                this.wakeWordRecognition.start();
                console.log('Wake word detection active - say "Hey AURA" or "AURA" to start');
            } catch (error) {
                console.error('Failed to start wake word detection:', error);
            }
        }
    }
    
    stopWakeWordDetection() {
        if (this.wakeWordRecognition && this.isWakeWordListening) {
            this.wakeWordRecognition.stop();
            this.isWakeWordListening = false;
        }
    }
    
    startListeningForCommand() {
        if (this.recognition && !this.isListening) {
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Failed to start command recognition:', error);
                setTimeout(() => this.startWakeWordDetection(), 1000);
            }
        }
    }
    
    setupEventListeners() {
        // File upload events
        this.uploadArea.addEventListener('click', () => this.imageInput.click());
        this.uploadArea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.imageInput.click();
            }
        });
        this.imageInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.uploadBtn.addEventListener('click', () => this.uploadImage());
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Model selection
        this.modelSelect.addEventListener('change', (e) => {
            this.selectedModel = e.target.value;
            this.updateModelInfo();
        });
        
        // Voice controls (voice-only interface)
        this.voiceToggle.addEventListener('click', () => this.toggleVoice());
        this.voiceInputToggle.addEventListener('click', () => this.toggleVoiceInput());
        this.stopBtn.addEventListener('click', () => this.stopCurrentAction());
    }
    
    updateAssistantStatus(state, text) {
        this.statusIndicator.className = `status-indicator ${state}`;
        this.statusText.textContent = text;
        
        if (this.sessionId) {
            fetch('/api/session/state', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId, state })
            }).catch(console.error);
        }
    }
    
    async updateDashboard() {
        try {
            const startTime = performance.now();
            const response = await fetch('/api/stats');
            const stats = await response.json();
            const loadTime = Math.round(performance.now() - startTime);
            
            if (this.globalImagesEl) {
                this.animateValue(this.globalImagesEl, stats.totalImages);
            }
            if (this.totalAnalysesEl) {
                this.animateValue(this.totalAnalysesEl, stats.totalAnalyses);
            }
            if (this.activeSessionsEl) {
                this.animateValue(this.activeSessionsEl, stats.activeSessions);
            }
            
            // Update connection status
            console.log(`📊 Dashboard updated in ${loadTime}ms`);
        } catch (error) {
            console.error('❌ Failed to update dashboard:', error);
            // Show connection issue in UI
            this.showStatus('Connection issue - retrying...', 'error');
        }
    }
    
    animateValue(element, targetValue) {
        if (!element) return;
        
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutCubic = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.floor(startValue + (targetValue - startValue) * easeOutCubic);
            
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    startListening() {
        if (this.recognition && !this.isListening) {
            this.stopWakeWordDetection();
            this.recognition.start();
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
        this.isListening = false;
        this.updateAssistantStatus('idle', 'AURA Ready - Say "Hey AURA"');
        this.stopBtn.style.display = 'none';
        
        if (this.voiceInputEnabled) {
            setTimeout(() => this.startWakeWordDetection(), 1000);
        }
    }
    
    stopCurrentAction() {
        if (this.isListening) {
            this.stopListening();
        }
        if (this.isSpeaking && this.audioElement) {
            this.audioElement.pause();
            this.isSpeaking = false;
            this.updateAssistantStatus('idle', 'AURA Ready');
        }
        
        if (this.voiceInputEnabled) {
            setTimeout(() => this.startWakeWordDetection(), 1000);
        }
    }
    
    toggleVoice() {
        this.voiceEnabled = !this.voiceEnabled;
        this.voiceToggle.classList.toggle('active', this.voiceEnabled);
    }
    
    toggleVoiceInput() {
        this.voiceInputEnabled = !this.voiceInputEnabled;
        this.voiceInputToggle.classList.toggle('active', this.voiceInputEnabled);
        
        if (this.voiceInputEnabled) {
            this.startWakeWordDetection();
            this.updateAssistantStatus('idle', 'AURA Ready - Say "Hey AURA"');
        } else {
            this.stopWakeWordDetection();
            this.updateAssistantStatus('idle', 'Voice detection disabled');
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            // Enhanced file validation
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];
            const maxSize = 10 * 1024 * 1024; // 10MB
            
            if (!validTypes.includes(file.type)) {
                this.showStatus('Please select a valid image file (JPG, PNG, WebP, or GIF)', 'error');
                return;
            }
            
            if (file.size > maxSize) {
                this.showStatus('File too large. Please select an image under 10MB.', 'error');
                return;
            }
            
            this.selectedFile = file;
            this.showFileInfo(file);
            this.uploadBtn.disabled = false;
            this.clearStatus();
        }
    }
    
    handleDragOver(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            
            // Same validation as file select
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];
            const maxSize = 10 * 1024 * 1024; // 10MB
            
            if (!validTypes.includes(file.type)) {
                this.showStatus('Please drop a valid image file (JPG, PNG, WebP, or GIF)', 'error');
                return;
            }
            
            if (file.size > maxSize) {
                this.showStatus('File too large. Please drop an image under 10MB.', 'error');
                return;
            }
            
            this.selectedFile = file;
            this.showFileInfo(file);
            this.uploadBtn.disabled = false;
            this.clearStatus();
        }
    }
    
    showFileInfo(file) {
        const sizeInKB = (file.size / 1024).toFixed(1);
        const sizeInMB = (file.size / 1024 / 1024).toFixed(2);
        const displaySize = file.size > 1024 * 1024 ? `${sizeInMB} MB` : `${sizeInKB} KB`;
        
        this.fileInfo.innerHTML = `
            <strong>${file.name}</strong><br>
            Size: ${displaySize} • Type: ${file.type.split('/')[1].toUpperCase()}
        `;
        this.fileInfo.style.display = 'block';
    }
    
    async uploadImage() {
        if (!this.selectedFile) return;
        
        this.uploadBtn.disabled = true;
        this.uploadBtn.innerHTML = '<div class="loading"></div> Uploading...';
        
        const formData = new FormData();
        formData.append('image', this.selectedFile);
        
        try {
            const response = await fetch('/api/upload-image', {
                method: 'POST',
                headers: {
                    'X-Session-ID': this.sessionId
                },
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.imageId = result.image_id;
                this.showStatus('Image uploaded successfully! Ready to analyze.', 'success');
                this.stopBtn.style.display = 'block';
                this.queryInput.focus();
                
                this.updateDashboard();
            } else {
                throw new Error(result.error || 'Upload failed');
            }
        } catch (error) {
            this.showStatus(`Upload failed: ${error.message}`, 'error');
        } finally {
            this.uploadBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Upload Image
            `;
            this.uploadBtn.disabled = false;
        }
    }
    
    async analyzeImage() {
        if (!this.imageId) {
            this.showStatus('Please upload an image first.', 'warning');
            return;
        }
        
        const query = this.queryInput.value.trim();
        if (!query) {
            this.showStatus('Please provide a question or wake word command.', 'warning');
            return;
        }
        
        this.updateAssistantStatus('processing', 'AURA Analyzing...');
        
        this.stopBtn.disabled = true;
        this.stopBtn.innerHTML = '<div class="loading"></div> Processing...';
        
        try {
            await this.analyzeImageWithRetry(this.selectedFile, query);
        } catch (error) {
            console.error('Analysis failed after retries:', error);
            this.showStatus('Analysis failed. Please try again.', 'error');
            this.updateAssistantStatus('idle', 'AURA Ready - Say "Hey AURA"');
        } finally {
            this.stopBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="6" y="6" width="12" height="12"/>
                </svg>
                Stop
            `;
            this.stopBtn.disabled = false;
            this.stopBtn.style.display = 'none';
        }
    }
    
    async analyzeImageWithRetry(imageFile, voiceText, maxRetries = 3) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                const formData = new FormData();
                formData.append('image', imageFile);
                formData.append('query', voiceText || 'Analyze this image');
                formData.append('model', this.selectedModel);

                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const result = await response.json();
                
                if (result.success) {
                    this.handleSuccessfulAnalysis(result);
                    return; // Success, exit retry loop
                } else {
                    throw new Error(result.error || 'Analysis failed');
                }
            } catch (error) {
                console.error(`Analysis attempt ${attempt} failed:`, error);
                
                if (attempt === maxRetries) {
                    throw error; // Final attempt failed
                }
                
                // Wait before retry (exponential backoff)
                const delay = Math.pow(2, attempt - 1) * 1000; // 1s, 2s, 4s
                this.showStatus(`Retrying... (attempt ${attempt + 1}/${maxRetries})`, 'info');
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }
    
    handleSuccessfulAnalysis(result) {
        this.displayAnalysisResult(result);
        this.queryInput.value = '';
        
        if (result.audio_url && this.voiceEnabled) {
            this.updateAssistantStatus('speaking', 'AURA Speaking...');
            this.playAudio(result.audio_url);
            this.updateAssistantStatus('idle', 'AURA Ready - Say "Hey AURA"');
        } else {
            this.updateAssistantStatus('idle', 'AURA Ready - Say "Hey AURA"');
        }
    }
    
    displayAnalysisResult(result) {
        let html = `
            <div class="result-card">
                <h3>Analysis Result</h3>
                <div style="line-height: 1.6;">${result.description}</div>
            </div>
        `;
        
        if (result.use_case_detected) {
            html += `
                <div class="analysis-metadata">
                    <div class="use-case-badge">${result.use_case_detected.replace('_', ' ').toUpperCase()}</div>
                    <strong>Model:</strong> ${result.model_used}<br>
                    <strong>Response Time:</strong> Optimized for speed<br>
                    <strong>Analysis Type:</strong> Casual & Conversational
                </div>
            `;
        }
        
        if (result.audio_url && this.voiceEnabled) {
            html += `
                <div class="audio-player">
                    <div>
                        <svg style="width: 16px; height: 16px; margin-right: 0.5rem;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                            <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/>
                        </svg>
                        Voice response available
                    </div>
                    <button class="play-btn" onclick="app.playAudio('${result.audio_url}')">
                        Play Audio
                    </button>
                </div>
            `;
        }
        
        this.analysisResult.innerHTML = html;
    }
    
    playAudio(audioUrl, casual = false) {
        if (this.audioElement) {
            this.audioElement.pause();
        }
        
        this.isSpeaking = true;
        const statusText = casual ? 'AURA Responding...' : 'AURA Speaking...';
        this.updateAssistantStatus('speaking', statusText);
        
        this.audioElement = new Audio(audioUrl);
        
        this.audioElement.onended = () => {
            this.isSpeaking = false;
            this.updateAssistantStatus('idle', 'AURA Ready');
        };
        
        this.audioElement.onerror = () => {
            this.isSpeaking = false;
            this.updateAssistantStatus('idle', 'AURA Ready');
            if (!casual) {
                this.showStatus('Audio playback failed', 'error');
            }
        };
        
        this.audioElement.play().catch(error => {
            console.error('Audio playback failed:', error);
            this.isSpeaking = false;
            this.updateAssistantStatus('idle', 'AURA Ready');
            if (!casual) {
                this.showStatus('Audio playback failed', 'error');
            }
        });
    }
    
    showStatus(message, type) {
        this.uploadStatus.innerHTML = `<div class="status ${type}">${message}</div>`;
    }
    
    clearStatus() {
        this.uploadStatus.innerHTML = '';
        this.analysisResult.innerHTML = '';
    }
}

// Initialize the application
let networkBackground;
let app;

document.addEventListener('DOMContentLoaded', () => {
    networkBackground = new NetworkBackground();
    app = new AuraVisionApp();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (networkBackground) {
        networkBackground.destroy();
    }
}); 