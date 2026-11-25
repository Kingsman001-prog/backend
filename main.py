from flask import *
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)




@app.route("/")
def index():
    return render_template("index.html")



@app.route("/submit", methods=['POST', 'GET'])
def Web():
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        print(f"Ip: {ip} \nPort: {port}")
        url = f"http://{ip}:{port}"
        try:
            response = requests.get(url, timeout=5)
            result = f" {response.text}"
            print(result)
            return render_template("index.html", result=result)
        except Exception as e:
            result = f"Connection: {e}"
            print(f"Error: {result}")
        return render_template("index.html", result=result)
        
    return render_template('index.html')
        
    
@app.route("/api", methods=['POST'])
def App():
    try:
        data = request.json
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
    app.run(debug=True, host="0.0.0.0", port=5000)