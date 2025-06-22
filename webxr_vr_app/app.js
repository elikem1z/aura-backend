// Aura VR WebXR Application
// Connects to FastAPI backend for voice-first image analysis

class AuraVRApp {
    constructor() {
        // Use network IP instead of localhost for cross-device access
        this.backendUrl = 'http://192.168.34.160:8001'; // Your FastAPI backend
        this.isConnected = false;
        this.currentImageId = null;
        this.sessionId = null;
        this.isProcessing = false;
        
        // WebXR components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        
        // Voice recognition
        this.recognition = null;
        this.isListening = false;
        
        // Device detection
        this.isVRSupported = this.checkVRSupport();
        this.isMobile = this.checkMobileDevice();
        
        console.log('📱 Device Info:', {
            isVRSupported: this.isVRSupported,
            isMobile: this.isMobile,
            userAgent: navigator.userAgent
        });
        
        this.init();
    }

    checkVRSupport() {
        const hasXR = 'xr' in navigator;
        const hasSessionSupport = navigator.xr && navigator.xr.isSessionSupported;
        
        console.log('🔍 VR Support Check:', {
            hasXR,
            hasSessionSupport,
            userAgent: navigator.userAgent
        });
        
        if (!hasXR || !hasSessionSupport) {
            return false;
        }
        
        // For now, we'll assume VR is supported if the basic APIs exist
        // In a real implementation, you'd want to check for specific VR capabilities
        return true;
    }

    checkMobileDevice() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
        
        console.log('📱 Mobile Check:', {
            userAgent: navigator.userAgent,
            screenWidth: window.innerWidth,
            isMobile
        });
        
        return isMobile;
    }

    async init() {
        try {
            console.log('🚀 Initializing Aura VR App...');
            
            // Initialize UI first
            this.initUI();
            
            // Initialize voice recognition
            this.initVoiceRecognition();
            
            // Initialize WebXR only if supported
            if (this.isVRSupported) {
                await this.initWebXR();
            } else {
                console.log('⚠️ WebXR not supported on this device');
                this.showNonVRMode();
            }
            
            console.log('✅ App initialization complete');
        } catch (error) {
            console.error('❌ App initialization failed:', error);
        }
    }

    showNonVRMode() {
        // Update UI for non-VR devices
        const uiContainer = document.getElementById('ui-container');
        const title = uiContainer.querySelector('h2');
        const info = uiContainer.querySelector('.info');
        const captureBtn = document.getElementById('capture-btn');
        
        if (this.isMobile) {
            title.textContent = '📱 Aura Mobile Assistant';
            captureBtn.innerHTML = '📷 Take Photo';
            info.innerHTML = `
                <p><strong>Mobile Mode:</strong></p>
                <p>1. Connect to your FastAPI backend</p>
                <p>2. Take a photo or upload an image</p>
                <p>3. Analyze the image or ask a voice question</p>
                <p>4. Listen to the AI's response</p>
            `;
        } else {
            title.textContent = '💻 Aura Desktop Assistant';
            captureBtn.innerHTML = '📁 Upload Image';
            info.innerHTML = `
                <p><strong>Desktop Mode:</strong></p>
                <p>1. Connect to your FastAPI backend</p>
                <p>2. Upload an image from your computer</p>
                <p>3. Analyze the image or ask a voice question</p>
                <p>4. Listen to the AI's response</p>
                <p><em>Note: VR features require a VR headset</em></p>
            `;
        }
        
        console.log('🖥️ Running in non-VR mode');
    }

    async initWebXR() {
        try {
            // Create scene
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(0x000000);

            // Create camera
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            this.camera.position.set(0, 1.6, 3);

            // Create renderer
            this.renderer = new THREE.WebGLRenderer({ antialias: true });
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setPixelRatio(window.devicePixelRatio);
            this.renderer.xr.enabled = true;
            document.getElementById('vr-scene').appendChild(this.renderer.domElement);

            // Add VR button only if VR is supported
            if (this.isVRSupported) {
                document.body.appendChild(VRButton.createButton(this.renderer));
            }

            // Add controls
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;

            // Add some basic geometry to the scene
            this.createScene();

            // Start render loop
            this.renderer.setAnimationLoop(() => {
                this.controls.update();
                this.renderer.render(this.scene, this.camera);
            });

            // Handle window resize
            window.addEventListener('resize', () => {
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(window.innerWidth, window.innerHeight);
            });

            console.log('✅ WebXR initialized successfully');
        } catch (error) {
            console.error('❌ Failed to initialize WebXR:', error);
        }
    }

    createScene() {
        // Add ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // Add directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        this.scene.add(directionalLight);

        // Add a simple cube
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x667eea,
            transparent: true,
            opacity: 0.8
        });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.set(0, 1.6, -2);
        this.scene.add(cube);

        // Add some floating spheres
        for (let i = 0; i < 5; i++) {
            const sphereGeometry = new THREE.SphereGeometry(0.2, 16, 16);
            const sphereMaterial = new THREE.MeshPhongMaterial({ 
                color: Math.random() * 0xffffff,
                transparent: true,
                opacity: 0.7
            });
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
            sphere.position.set(
                (Math.random() - 0.5) * 10,
                Math.random() * 5,
                (Math.random() - 0.5) * 10
            );
            this.scene.add(sphere);
        }
    }

    initVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                console.log('🎤 Voice recognition started');
                this.isListening = true;
                this.updateStatus('🎤 Listening...', 'processing');
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('🎤 Voice input:', transcript);
                this.processVoiceQuery(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('🎤 Voice recognition error:', event.error);
                this.isListening = false;
                this.updateStatus('🔴 Voice recognition failed', 'disconnected');
            };

            this.recognition.onend = () => {
                console.log('🎤 Voice recognition ended');
                this.isListening = false;
                if (this.isConnected) {
                    this.updateStatus('🟢 Connected to Backend', 'connected');
                }
            };
        } else {
            console.warn('⚠️ Speech recognition not supported');
        }
    }

    initUI() {
        // Add VR UI toggle
        document.addEventListener('keydown', (event) => {
            if (event.key === 'v' || event.key === 'V') {
                this.toggleVRUI();
            }
        });

        // Add controller support for VR
        this.renderer.xr.addEventListener('sessionstart', () => {
            console.log('🎮 VR session started');
            this.showVRUI();
        });

        this.renderer.xr.addEventListener('sessionend', () => {
            console.log('🎮 VR session ended');
            this.hideVRUI();
        });
    }

    async testBackendConnection() {
        try {
            const response = await fetch(`${this.backendUrl}/ping`);
            if (response.ok) {
                console.log('✅ Backend connection test successful');
                this.updateStatus('🟢 Backend Available', 'connected');
            } else {
                console.log('⚠️ Backend connection test failed');
                this.updateStatus('🔴 Backend Unavailable', 'disconnected');
            }
        } catch (error) {
            console.error('❌ Backend connection test error:', error);
            this.updateStatus('🔴 Backend Unavailable', 'disconnected');
        }
    }

    async connectToBackend() {
        try {
            this.updateStatus('🔄 Connecting...', 'processing');
            
            // Test connection
            const response = await fetch(`${this.backendUrl}/ping`);
            if (!response.ok) {
                throw new Error('Backend not responding');
            }

            // Create session
            const sessionResponse = await fetch(`${this.backendUrl}/voice/session/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: `vr_user_${Date.now()}`
                })
            });

            if (sessionResponse.ok) {
                const sessionData = await sessionResponse.json();
                this.sessionId = sessionData.session_id;
                this.isConnected = true;
                this.updateStatus('🟢 Connected to Backend', 'connected');
                this.enableButtons();
                console.log('✅ Connected to backend with session:', this.sessionId);
            } else {
                throw new Error('Failed to create session');
            }
        } catch (error) {
            console.error('❌ Connection failed:', error);
            this.updateStatus('🔴 Connection Failed', 'disconnected');
            this.isConnected = false;
            this.disableButtons();
        }
    }

    async captureScreenshot() {
        if (!this.isConnected) {
            alert('Please connect to backend first');
            return;
        }

        console.log('📸 Screenshot attempt - Device info:', {
            isMobile: this.isMobile,
            isVRSupported: this.isVRSupported,
            hasRenderer: !!this.renderer,
            hasDomElement: !!(this.renderer && this.renderer.domElement)
        });

        // For mobile devices, use file upload
        if (this.isMobile) {
            console.log('📱 Mobile device detected, using file upload');
            this.uploadImageFromDevice();
            return;
        }

        // For desktop/PC without VR, offer file upload option
        if (!this.isVRSupported || !this.renderer || !this.renderer.domElement) {
            console.log('📱 No VR renderer available, using file upload');
            this.uploadImageFromDevice();
            return;
        }

        try {
            this.updateStatus('📸 Capturing screenshot...', 'processing');
            
            // Check if renderer has content
            const canvas = this.renderer.domElement;
            console.log('🎨 Canvas info:', {
                width: canvas.width,
                height: canvas.height,
                hasContent: canvas.width > 0 && canvas.height > 0
            });
            
            if (!canvas || canvas.width === 0 || canvas.height === 0) {
                console.log('⚠️ Renderer canvas is empty, using file upload instead');
                this.uploadImageFromDevice();
                return;
            }
            
            // Capture the current view
            const dataURL = canvas.toDataURL('image/jpeg', 0.8);
            console.log('📸 Screenshot captured, size:', dataURL.length);
            
            // Convert to blob
            const response = await fetch(dataURL);
            const blob = await response.blob();
            console.log('📦 Blob created, size:', blob.size);
            
            // Create form data
            const formData = new FormData();
            formData.append('image', blob, 'vr_screenshot.jpg');
            formData.append('user_id', `vr_user_${Date.now()}`);
            formData.append('session_id', this.sessionId);

            // Upload to backend
            const uploadResponse = await fetch(`${this.backendUrl}/upload-image`, {
                method: 'POST',
                body: formData
            });

            if (uploadResponse.ok) {
                const uploadData = await uploadResponse.json();
                this.currentImageId = uploadData.image_id;
                this.updateStatus('✅ Screenshot uploaded', 'connected');
                console.log('✅ Screenshot uploaded:', this.currentImageId);
                
                // Enable analyze button
                document.getElementById('analyze-btn').disabled = false;
            } else {
                const errorText = await uploadResponse.text();
                throw new Error(`Upload failed: ${errorText}`);
            }
        } catch (error) {
            console.error('❌ Screenshot capture failed:', error);
            this.updateStatus('🔴 Screenshot failed - trying file upload', 'disconnected');
            
            // Fallback to file upload if screenshot fails
            setTimeout(() => {
                this.uploadImageFromDevice();
            }, 1000);
        }
    }

    uploadImageFromDevice() {
        // Create a file input element
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        
        // Use camera on mobile, file picker on desktop
        if (this.isMobile) {
            fileInput.capture = 'environment';
        }
        
        fileInput.onchange = async (event) => {
            const file = event.target.files[0];
            if (!file) {
                this.updateStatus('❌ No file selected', 'disconnected');
                return;
            }

            try {
                this.updateStatus('📸 Uploading image...', 'processing');
                
                // Create form data
                const formData = new FormData();
                formData.append('image', file);
                formData.append('user_id', this.isMobile ? `mobile_user_${Date.now()}` : `desktop_user_${Date.now()}`);
                formData.append('session_id', this.sessionId);

                // Upload to backend
                const uploadResponse = await fetch(`${this.backendUrl}/upload-image`, {
                    method: 'POST',
                    body: formData
                });

                if (uploadResponse.ok) {
                    const uploadData = await uploadResponse.json();
                    this.currentImageId = uploadData.image_id;
                    this.updateStatus('✅ Image uploaded successfully', 'connected');
                    console.log('✅ Image uploaded:', this.currentImageId);
                    
                    // Enable analyze button
                    document.getElementById('analyze-btn').disabled = false;
                } else {
                    const errorText = await uploadResponse.text();
                    throw new Error(`Upload failed: ${errorText}`);
                }
            } catch (error) {
                console.error('❌ Image upload failed:', error);
                this.updateStatus(`🔴 Upload failed: ${error.message}`, 'disconnected');
            }
        };

        // Show user-friendly message
        if (this.isMobile) {
            this.updateStatus('📱 Opening camera...', 'processing');
        } else {
            this.updateStatus('💻 Select an image file...', 'processing');
        }

        // Trigger file selection
        fileInput.click();
    }

    async analyzeImage() {
        if (!this.currentImageId) {
            alert('Please capture a screenshot first');
            return;
        }

        try {
            this.updateStatus('🔍 Analyzing image...', 'processing');
            
            const response = await fetch(`${this.backendUrl}/analyze-image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_id: this.currentImageId,
                    query: 'What do you see in this image? Please describe it in detail for someone who is visually impaired.',
                    session_id: this.sessionId
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.updateStatus('✅ Analysis complete', 'connected');
                console.log('✅ Analysis result:', data);
                
                // Play audio response
                if (data.audio_url) {
                    await this.playAudioResponse(data.audio_url);
                }
            } else {
                throw new Error('Analysis failed');
            }
        } catch (error) {
            console.error('❌ Image analysis failed:', error);
            this.updateStatus('🔴 Analysis failed', 'disconnected');
        }
    }

    async startVoiceQuery() {
        if (!this.currentImageId) {
            alert('Please capture a screenshot first');
            return;
        }

        if (!this.recognition) {
            alert('Voice recognition not supported in this browser');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('❌ Failed to start voice recognition:', error);
            this.updateStatus('🔴 Voice recognition failed', 'disconnected');
        }
    }

    async processVoiceQuery(transcript) {
        try {
            this.updateStatus('🔍 Processing voice query...', 'processing');
            
            const response = await fetch(`${this.backendUrl}/analyze-image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_id: this.currentImageId,
                    query: transcript,
                    session_id: this.sessionId
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.updateStatus('✅ Voice query processed', 'connected');
                console.log('✅ Voice query result:', data);
                
                // Play audio response
                if (data.audio_url) {
                    await this.playAudioResponse(data.audio_url);
                }
            } else {
                throw new Error('Voice query processing failed');
            }
        } catch (error) {
            console.error('❌ Voice query processing failed:', error);
            this.updateStatus('🔴 Voice query failed', 'disconnected');
        }
    }

    async playAudioResponse(audioUrl) {
        try {
            const audioPlayer = document.getElementById('audio-player');
            const audioContainer = document.getElementById('audio-container');
            
            audioPlayer.src = `${this.backendUrl}${audioUrl}`;
            audioContainer.style.display = 'block';
            
            // Auto-play the audio
            await audioPlayer.play();
            
            console.log('🎵 Playing audio response');
        } catch (error) {
            console.error('❌ Failed to play audio:', error);
        }
    }

    updateStatus(message, type) {
        const statusElement = document.getElementById('status');
        statusElement.textContent = message;
        statusElement.className = `status ${type}`;
    }

    enableButtons() {
        document.getElementById('capture-btn').disabled = false;
        document.getElementById('voice-btn').disabled = false;
    }

    disableButtons() {
        document.getElementById('capture-btn').disabled = true;
        document.getElementById('analyze-btn').disabled = true;
        document.getElementById('voice-btn').disabled = true;
    }

    toggleVRUI() {
        const vrUI = document.getElementById('vr-ui');
        if (vrUI.classList.contains('active')) {
            this.hideVRUI();
        } else {
            this.showVRUI();
        }
    }

    showVRUI() {
        const vrUI = document.getElementById('vr-ui');
        vrUI.classList.add('active');
    }

    hideVRUI() {
        const vrUI = document.getElementById('vr-ui');
        vrUI.classList.remove('active');
    }
}

// Global functions for HTML onclick handlers
let auraApp;

window.onload = () => {
    auraApp = new AuraVRApp();
};

function connectToBackend() {
    if (auraApp) {
        auraApp.connectToBackend();
    }
}

function captureScreenshot() {
    if (auraApp) {
        auraApp.captureScreenshot();
    }
}

function analyzeImage() {
    if (auraApp) {
        auraApp.analyzeImage();
    }
}

function startVoiceQuery() {
    if (auraApp) {
        auraApp.startVoiceQuery();
    }
}

function hideVRUI() {
    if (auraApp) {
        auraApp.hideVRUI();
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuraVRApp;
} 