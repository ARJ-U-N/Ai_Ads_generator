from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)


# ⚠️ UPDATE THIS WITH YOUR NGROK URL FROM COLAB!
API_URL = "https://unevinced-adrianna-villously.ngrok-free.dev"


# ================================
# ROUTES
# ================================


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tool1')
def tool1():
    return render_template('tool1.html')


@app.route('/tool2')
def tool2():
    return render_template('tool2.html')


@app.route('/tool3')
def tool3():
    return render_template('tool3.html')


@app.route('/tool4')
def tool4():
    return render_template('tool4.html')


# ================================
# API PROXY ENDPOINTS (WITH ERROR HANDLING)
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
            timeout=120
        )
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error")
        return jsonify({
            "success": False, 
            "error": "Request timeout. Try again."
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


@app.route('/api/animate-image', methods=['POST'])
def proxy_animate_image():
    """Proxy to Colab API - Tool 2 (VIDEO)"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 2 (Video Animation)")
        print(f"⏱️  This takes 3-5 minutes, please wait...")
        
        response = requests.post(
            f"{API_URL}/api/animate-image",
            json={"ai_image": data.get('ai_image')},
            timeout=600  # 10 minutes
        )
        
        # Check if response is empty (Colab crashed)
        if not response.text or response.text.strip() == '':
            print("❌ Empty response from Colab (likely crashed)")
            return jsonify({
                "success": False,
                "error": "Colab crashed during video generation. Restart the Colab runtime and try again."
            }), 500
        
        # Try to parse JSON
        try:
            result = response.json()
        except ValueError as json_error:
            print(f"❌ Invalid JSON response: {response.text[:200]}")
            return jsonify({
                "success": False,
                "error": f"Colab returned invalid response. Preview: {response.text[:100]}"
            }), 500
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(result)
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error after 10 minutes")
        return jsonify({
            "success": False,
            "error": "Request timeout after 10 minutes. Restart Colab."
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
    """Proxy to Colab API - Tool 3"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 3: Avatar #{data.get('avatar_id')}")
        print(f"⏱️  This generates both image AND video, takes 4-6 minutes...")
        
        response = requests.post(
            f"{API_URL}/api/generate-avatar",
            json=data,
            timeout=600
        )
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error after 10 minutes")
        return jsonify({
            "success": False,
            "error": "Request timeout. Try simpler description."
        }), 504
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/enhance-image', methods=['POST'])
def proxy_enhance_image():
    """Proxy to Colab API - Tool 4 (Image Enhancement)"""
    try:
        data = request.json
        print(f"📨 Received request for Tool 4 (Image Enhancement)")
        print(f"   Description: {data.get('description', 'professional product photography')[:50]}...")
        print(f"   Strength: {data.get('strength', 0.75)}")
        
        response = requests.post(
            f"{API_URL}/api/enhance-image",
            json=data,
            timeout=120
        )
        
        # Check if response is empty
        if not response.text or response.text.strip() == '':
            print("❌ Empty response from Colab")
            return jsonify({
                "success": False,
                "error": "Empty response from Colab. Check if models are loaded."
            }), 500
        
        # Try to parse JSON
        try:
            result = response.json()
        except ValueError:
            print(f"❌ Invalid JSON response: {response.text[:200]}")
            return jsonify({
                "success": False,
                "error": f"Invalid JSON from Colab: {response.text[:100]}"
            }), 500
        
        print(f"✅ Response status: {response.status_code}")
        return jsonify(result)
        
    except requests.exceptions.Timeout:
        print("❌ Timeout error")
        return jsonify({
            "success": False,
            "error": "Request timeout. Image enhancement took too long."
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


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI Product Ad Generator - Frontend")
    print("="*60)
    print(f"📡 Colab API: {API_URL}")
    print(f"🌐 Frontend: http://localhost:5001")
    print("="*60)
    print("\n📋 Available Tools:")
    print("   Tool 1: Generate Image (text → image)")
    print("   Tool 2: Animate Video (image → video)")
    print("   Tool 3: Avatar Product (text → image + video)")
    print("   Tool 4: Enhance Image (image → enhanced image)")
    print("="*60)
    print("\n⚠️  IMPORTANT:")
    print("   - Make sure Colab is running")
    print("   - Update API_URL with your ngrok URL")
    print("   - Video generation takes 3-5 minutes")
    print("   - Image enhancement takes 15-25 seconds")
    print("="*60)
    print("\n✅ Starting Flask server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
