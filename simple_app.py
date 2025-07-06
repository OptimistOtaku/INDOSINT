#!/usr/bin/env python3
"""
INDOSINT - Indian OSINT Platform (Simplified Version)
A working prototype with core features
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import random
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

# Mock data storage
digital_footprints = {}

# Regional language support
LANGUAGE_KEYWORDS = {
    "hi": ["नाम", "पता", "फोन", "ईमेल", "कंपनी"],
    "bn": ["নাম", "ঠিকানা", "ফোন", "ইমেইল", "কোম্পানি"],
    "ta": ["பெயர்", "முகவரி", "தொலைபேசி", "மின்னஞ்சல்", "நிறுவனம்"],
    "te": ["పేరు", "చిరునామా", "ఫోన్", "ఇమెయిల్", "కంపెనీ"],
    "mr": ["नाव", "पत्ता", "फोन", "ईमेल", "कंपनी"],
    "gu": ["નામ", "સરનામું", "ફોન", "ઈમેલ", "કંપની"]
}

def search_social_media(query, platforms, language="en"):
    """Search for person across social media platforms"""
    results = []
    
    for platform in platforms:
        if platform == "twitter":
            mock_result = {
                "platform": "Twitter",
                "username": f"@{query.lower().replace(' ', '')}",
                "profile_url": f"https://twitter.com/{query.lower().replace(' ', '')}",
                "bio": f"Digital enthusiast | Tech lover | {query}",
                "followers": random.randint(100, 10000),
                "posts": random.randint(50, 500),
                "last_active": datetime.now().isoformat(),
                "confidence": 0.85
            }
            results.append(mock_result)
        
        elif platform == "linkedin":
            mock_result = {
                "platform": "LinkedIn",
                "username": query,
                "profile_url": f"https://linkedin.com/in/{query.lower().replace(' ', '-')}",
                "bio": f"Professional at Tech Company | {query}",
                "followers": random.randint(50, 5000),
                "posts": random.randint(10, 100),
                "last_active": datetime.now().isoformat(),
                "confidence": 0.90
            }
            results.append(mock_result)
        
        elif platform == "facebook":
            mock_result = {
                "platform": "Facebook",
                "username": query,
                "profile_url": f"https://facebook.com/{query.lower().replace(' ', '.')}",
                "bio": f"Living life to the fullest | {query}",
                "followers": random.randint(200, 2000),
                "posts": random.randint(100, 1000),
                "last_active": datetime.now().isoformat(),
                "confidence": 0.75
            }
            results.append(mock_result)
    
    return results

def analyze_digital_footprint(person_data):
    """Analyze digital footprint of a person"""
    social_presence = search_social_media(
        person_data["name"], 
        ["twitter", "linkedin", "facebook"]
    )
    
    # Mock email breach data
    email_breaches = []
    if person_data.get("email"):
        email_breaches = [
            {
                "breach_name": "MockBreach2023",
                "date": "2023-06-15",
                "data_types": ["email", "password", "name"],
                "severity": "medium"
            }
        ]
    
    # Mock domain registrations
    domain_registrations = []
    if person_data.get("name"):
        domain_registrations = [
            {
                "domain": f"{person_data['name'].lower().replace(' ', '')}.com",
                "registration_date": "2022-01-15",
                "expiry_date": "2024-01-15",
                "registrar": "GoDaddy"
            }
        ]
    
    # Calculate risk score
    risk_score = 0.3  # Base risk
    if email_breaches:
        risk_score += 0.3
    if len(social_presence) > 2:
        risk_score += 0.2
    if domain_registrations:
        risk_score += 0.2
    
    return {
        "person": person_data,
        "social_presence": social_presence,
        "email_breaches": email_breaches,
        "domain_registrations": domain_registrations,
        "risk_score": min(risk_score, 1.0)
    }

def face_recognition_search(image_data):
    """Perform face recognition search"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_bytes))
        
        # Mock face detection
        image_array = np.array(image)
        num_faces = min(2, max(1, (image_array.shape[0] * image_array.shape[1]) // 100000))
        
        # Mock face recognition results
        results = []
        for i in range(num_faces):
            mock_matches = [
                {
                    "name": "John Doe",
                    "confidence": 0.85,
                    "source": "LinkedIn Profile",
                    "url": "https://linkedin.com/in/johndoe"
                },
                {
                    "name": "Jane Smith",
                    "confidence": 0.72,
                    "source": "Twitter Profile",
                    "url": "https://twitter.com/janesmith"
                }
            ]
            
            results.append({
                "face_id": i,
                "location": [100, 100, 200, 200],
                "matches": mock_matches
            })
        
        return {
            "faces_detected": num_faces,
            "results": results
        }
        
    except Exception as e:
        return {"error": f"Face recognition failed: {str(e)}"}

def translate_query(query, target_language):
    """Translate query to regional language"""
    if target_language in LANGUAGE_KEYWORDS:
        translated = query
        for keyword in LANGUAGE_KEYWORDS[target_language]:
            if keyword.lower() in query.lower():
                translated = f"{translated} ({keyword})"
        return translated
    return query

# API Routes
@app.route('/')
def root():
    return jsonify({
        "message": "INDOSINT - Indian OSINT Platform",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/search/social-media', methods=['POST'])
def social_media_search():
    """Search for person across social media platforms"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        platforms = data.get('platforms', ['twitter', 'linkedin', 'facebook'])
        language = data.get('language', 'en')
        
        results = search_social_media(query, platforms, language)
        
        return jsonify({
            "query": query,
            "results": results,
            "total_results": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/footprint', methods=['POST'])
def analyze_footprint():
    """Analyze digital footprint of a person"""
    try:
        person_data = request.get_json()
        footprint = analyze_digital_footprint(person_data)
        
        # Store footprint
        if person_data.get('name'):
            digital_footprints[person_data['name']] = footprint
        
        return jsonify({
            "footprint": footprint,
            "message": "Analysis completed successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search/face-recognition', methods=['POST'])
def face_recognition_endpoint():
    """Perform face recognition search"""
    try:
        image_data = request.get_json()
        results = face_recognition_search(image_data)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate_endpoint():
    """Translate query to regional language"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        target_language = data.get('target_language', 'en')
        
        translated = translate_query(query, target_language)
        
        return jsonify({
            "original": query,
            "translated": translated,
            "target_language": target_language
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/footprints')
def get_footprints():
    """Get all analyzed digital footprints"""
    return jsonify({
        "footprints": list(digital_footprints.keys())
    })

@app.route('/footprints/<name>')
def get_footprint(name):
    """Get specific digital footprint"""
    if name not in digital_footprints:
        return jsonify({"error": "Footprint not found"}), 404
    
    return jsonify({
        "footprint": digital_footprints[name]
    })

# Simple HTML interface for testing
@app.route('/test')
def test_interface():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>INDOSINT - Test Interface</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 INDOSINT - Test Interface</h1>
            
            <h2>Social Media Search</h2>
            <div class="form-group">
                <label>Search Query:</label>
                <input type="text" id="searchQuery" placeholder="Enter name to search...">
            </div>
            <div class="form-group">
                <label>Language:</label>
                <select id="language">
                    <option value="en">English</option>
                    <option value="hi">Hindi</option>
                    <option value="bn">Bengali</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                    <option value="mr">Marathi</option>
                    <option value="gu">Gujarati</option>
                </select>
            </div>
            <button onclick="searchSocialMedia()">Search</button>
            <div id="searchResult" class="result"></div>
            
            <h2>Digital Footprint Analysis</h2>
            <div class="form-group">
                <label>Name:</label>
                <input type="text" id="footprintName" placeholder="Enter full name...">
            </div>
            <div class="form-group">
                <label>Email:</label>
                <input type="email" id="footprintEmail" placeholder="Enter email...">
            </div>
            <button onclick="analyzeFootprint()">Analyze</button>
            <div id="footprintResult" class="result"></div>
        </div>
        
        <script>
            async function searchSocialMedia() {
                const query = document.getElementById('searchQuery').value;
                const language = document.getElementById('language').value;
                
                try {
                    const response = await fetch('/search/social-media', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            query: query,
                            platforms: ['twitter', 'linkedin', 'facebook'],
                            language: language
                        })
                    });
                    
                    const data = await response.json();
                    document.getElementById('searchResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('searchResult').innerHTML = 'Error: ' + error.message;
                }
            }
            
            async function analyzeFootprint() {
                const name = document.getElementById('footprintName').value;
                const email = document.getElementById('footprintEmail').value;
                
                try {
                    const response = await fetch('/analyze/footprint', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            name: name,
                            email: email
                        })
                    });
                    
                    const data = await response.json();
                    document.getElementById('footprintResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('footprintResult').innerHTML = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    print("🔍 Starting INDOSINT - Indian OSINT Platform")
    print("=" * 50)
    print("Backend API will be available at: http://localhost:5000")
    print("Test Interface: http://localhost:5000/test")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True) 