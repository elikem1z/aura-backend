from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai
from gtts import gTTS
import io
import tempfile
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# API configurations
BIBLE_API_KEY = os.getenv('BIBLE_API_KEY', 'a1692756d99fab00256e70dbda406cc7')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
BIBLIA_BASE_URL = "https://api.biblia.com/v1"
BIBLE_API_BASE_URL = "https://bible-api.com"

# Initialize Gemini AI
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini AI initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Gemini AI: {e}")
        model = None

class IntelligentBibleSearch:
    """Enhanced Bible search with LLM capabilities"""
    
    def __init__(self):
        self.biblia_key = BIBLE_API_KEY
        self.conversation_history = []
        
    def search_biblia(self, query, translation="kjv"):
        """Search using Biblia.com API"""
        try:
            url = f"{BIBLIA_BASE_URL}/bible/search/{translation}.txt"
            params = {
                'query': query,
                'key': self.biblia_key
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Biblia API error: {e}")
            return None
    
    def search_bible_api(self, query):
        """Search using bible-api.com"""
        try:
            url = f"{BIBLE_API_BASE_URL}/{query}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Bible API error: {e}")
            return None
    
    def process_with_llm(self, user_input, bible_results):
        """Process user input and Bible results with LLM"""
        if not model:
            return {
                'explanation': 'AI analysis not available. Please check your Gemini API key configuration.',
                'refined_query': user_input,
                'reasoning': 'LLM not configured or API key invalid.',
                'confidence': 'Low'
            }
        
        try:
            # Create context for the LLM
            context = f"""
            User Query: "{user_input}"
            
            Bible Search Results:
            {json.dumps(bible_results, indent=2)}
            
            Task: Analyze the user's query and Bible results to:
            1. Understand what the user is looking for
            2. Refine the search query if needed
            3. Explain the relevant verses found
            4. Provide reasoning for the search results
            
            Respond in JSON format:
            {{
                "explanation": "Clear explanation of what was found and why it's relevant",
                "refined_query": "Improved search query if needed",
                "reasoning": "Step-by-step reasoning of the search process",
                "confidence": "High/Medium/Low confidence in the results"
            }}
            """
            
            response = model.generate_content(context)
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            print(f"LLM processing error: {e}")
            return {
                'explanation': f'AI analysis temporarily unavailable. Please try again later.',
                'refined_query': user_input,
                'reasoning': f'LLM processing failed: {str(e)}',
                'confidence': 'Low'
            }
    
    def generate_voice_response(self, text):
        """Generate speech from text"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception as e:
            print(f"TTS error: {e}")
            return None
    
    def intelligent_search(self, user_input):
        """Main intelligent search function"""
        # Step 1: Initial Bible search
        bible_results = {
            'biblia': self.search_biblia(user_input),
            'bible_api': self.search_bible_api(user_input),
            'query': user_input
        }
        
        # Step 2: Process with LLM
        llm_analysis = self.process_with_llm(user_input, bible_results)
        
        # Step 3: If LLM suggests refined query, search again
        refined_results = None
        if llm_analysis.get('refined_query') and llm_analysis['refined_query'] != user_input:
            refined_results = {
                'biblia': self.search_biblia(llm_analysis['refined_query']),
                'bible_api': self.search_bible_api(llm_analysis['refined_query']),
                'query': llm_analysis['refined_query']
            }
        
        return {
            'original_query': user_input,
            'bible_results': bible_results,
            'refined_results': refined_results,
            'llm_analysis': llm_analysis,
            'conversation_history': self.conversation_history
        }

# Initialize intelligent search
intelligent_search = IntelligentBibleSearch()

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    return '', 204  # No content response

@app.route('/')
def index():
    """Serve the main application"""
    return render_template('index.html')

@app.route('/api/intelligent-search', methods=['POST'])
def intelligent_search_endpoint():
    """Intelligent search with LLM processing"""
    try:
        data = request.get_json()
        user_input = data.get('query', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform intelligent search
        results = intelligent_search.intelligent_search(user_input)
        
        # Add to conversation history
        intelligent_search.conversation_history.append({
            'user_input': user_input,
            'results': results,
            'timestamp': str(datetime.now())
        })
        
        # Limit conversation history
        if len(intelligent_search.conversation_history) > 10:
            intelligent_search.conversation_history.pop(0)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Handle speech input and process with LLM"""
    try:
        data = request.get_json()
        speech_text = data.get('speech_text', '').strip()
        
        if not speech_text:
            return jsonify({'error': 'Speech text is required'}), 400
        
        # Process speech input intelligently
        results = intelligent_search.intelligent_search(speech_text)
        
        return jsonify({
            'success': True,
            'speech_text': speech_text,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Generate speech
        audio_data = intelligent_search.generate_voice_response(text)
        
        if audio_data:
            return send_file(
                audio_data,
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name='response.mp3'
            )
        else:
            return jsonify({'error': 'Failed to generate speech'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_verses():
    """Legacy search endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Use intelligent search
        results = intelligent_search.intelligent_search(query)
        
        return jsonify({
            'success': True,
            'results': results,
            'query': query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation-history')
def get_conversation_history():
    """Get conversation history"""
    return jsonify({
        'history': intelligent_search.conversation_history
    })

@app.route('/api/clear-history', methods=['POST'])
def clear_conversation_history():
    """Clear conversation history"""
    intelligent_search.conversation_history = []
    return jsonify({'success': True, 'message': 'History cleared'})

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    llm_status = 'configured' if model else 'not_configured'
    return jsonify({
        'status': 'healthy', 
        'message': 'Intelligent Bible Search API is running',
        'llm_status': llm_status
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode) 