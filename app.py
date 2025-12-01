from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your Colab API URL - UPDATE THIS WITH YOUR NGROK URL!
API_URL = "https://unevinced-adrianna-villously.ngrok-free.dev"

# ================================
# ROUTES
# ================================

@app.route('/')
def home():
    """Home page with 3 tool cards"""
    return render_template('home.html')

@app.route('/tool1')
def tool1():
    """Tool 1: Generate Product Image"""
    return render_template('tool1.html')

@app.route('/tool2')
def tool2():
    """Tool 2: Animate Product Video"""
    return render_template('tool2.html')

@app.route('/tool3')
def tool3():
    """Tool 3: Product with Avatar"""
    return render_template('tool3.html')

# ================================
# API PROXY ENDPOINTS
# ================================

@app.route('/api/generate-image', methods=['POST'])
def proxy_generate_image():
    """Proxy to Colab API - Tool 1"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 1: {data.get('description', 'No description')[:50]}...")
        
        response = requests.post(
            f"{API_URL}/api/generate-image",
            json=data,
            timeout=120  # 2 minutes for image generation
        )
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error")
        return jsonify({
            "success": False, 
            "error": "Request timeout. Image generation is taking too long. Try again."
        }), 504
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return jsonify({
            "success": False,
            "error": "Cannot connect to Colab API. Make sure Colab is running and ngrok URL is correct."
        }), 503
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500

@app.route('/api/animate-image', methods=['POST'])
def proxy_animate_image():
    """Proxy to Colab API - Tool 2 (VIDEO - LONG TIMEOUT!)"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 2 (Video Animation)")
        print(f"⏱️  This takes 3-5 minutes, please wait...")
        
        response = requests.post(
            f"{API_URL}/api/animate-image",
            json={"ai_image": data.get('ai_image')},
            timeout=600  # 10 MINUTES for video generation!
        )
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error after 10 minutes")
        return jsonify({
            "success": False,
            "error": "Request timeout after 10 minutes. Video generation failed. Try restarting Colab."
        }), 504
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return jsonify({
            "success": False,
            "error": "Cannot connect to Colab API. Make sure Colab is running."
        }), 503
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/generate-avatar', methods=['POST'])
def proxy_generate_avatar():
    """Proxy to Colab API - Tool 3 (IMAGE + VIDEO - VERY LONG TIMEOUT!)"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 3: Avatar #{data.get('avatar_id')}")
        print(f"⏱️  This generates both image AND video, takes 4-6 minutes...")
        
        response = requests.post(
            f"{API_URL}/api/generate-avatar",
            json=data,
            timeout=600  # 10 MINUTES for avatar + video!
        )
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error after 10 minutes")
        return jsonify({
            "success": False,
            "error": "Request timeout after 10 minutes. Avatar generation failed. Try simpler product description."
        }), 504
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return jsonify({
            "success": False,
            "error": "Cannot connect to Colab API. Make sure Colab is running."
        }), 503
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ================================
# HEALTH CHECK
# ================================

@app.route('/health')
def health():
    """Check if API is reachable"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        return jsonify({
            "status": "healthy",
            "colab_api": "connected",
            "colab_response": response.json()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "colab_api": "disconnected",
            "error": str(e)
        }), 503

# ================================
# ERROR HANDLERS
# ================================

@app.errorhandler(404)
def not_found(e):
    return render_template('home.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ================================
# RUN APP
# ================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI Product Ad Generator - Frontend")
    print("="*60)
    print(f"📡 Colab API: {API_URL}")
    print(f"🌐 Frontend: http://localhost:5001")
    print("="*60)
    print("\n⚠️  IMPORTANT:")
    print("   - Make sure Colab is running")
    print("   - Update API_URL with your ngrok URL")
    print("   - Video generation takes 3-5 minutes")
    print("="*60)
    print("\n✅ Starting Flask server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
