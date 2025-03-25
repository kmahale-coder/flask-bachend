from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # 👈 CORS import karna mat bhoolo
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # 👈 CORS enable karo (sab allowed origins ke liye)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    quality = data.get('quality')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    output_filename = 'downloaded_video.mp4'  # 👈 Ensure karo ki filename correct ho
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': output_filename,  
        'merge_output_format': 'mp4'  # 👈 Ensure MP4 output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_filename, as_attachment=True, mimetype='video/mp4')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
