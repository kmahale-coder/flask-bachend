#backend 


from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 CORS Import Karo

app = Flask(__name__)
CORS(app)  # 👈 Ye CORS ko enable karega sabhi domains ke liye

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality")

    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Yahan tumhara YouTube download logic hoga

    return jsonify({"message": "Download started!"})

if __name__ == '__main__':
    app.run(debug=True)


