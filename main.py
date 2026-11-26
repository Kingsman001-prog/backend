from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST', 'GET'])
def Web():
    result = ""
    if request.method == 'POST':
        ip = request.form.get('ip')
        port = request.form.get('port')
        print(f"Ip: {ip} Port: {port}")
        url = f"http://{ip}:{port}/"
        try:
            response = requests.get(url, timeout=5)
            result = response.text
            print(result)
        except Exception as e:
            result = f"Connection: {e}"
            print(f"Error: {result}")
    return render_template("index.html", result=result)

@app.route("/api", methods=['POST'])
def App():
    try:
        data = request.get_json(force=True)
        ip = data.get("ip")
        port = data.get("port")
        print(f"Received from App: {ip}:{port}")
        url = f"http://{ip}:{port}/"
        response = requests.get(url, timeout=5)
        return jsonify({"status": 200, "message": "successful", "arduino_data": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": 500, "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)