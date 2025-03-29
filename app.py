# Backend (Flask) for YouTube Video Downloading

from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/get_qualities', methods=['POST'])
def get_qualities():
    try:
        data = request.json
        video_url = data.get('url')
        if not video_url:
            return jsonify({"error": "URL is required"}), 400

        yt = YouTube(video_url)
        qualities = [{"resolution": stream.resolution, "itag": stream.itag} for stream in yt.streams.filter(progressive=True, file_extension="mp4")]
        return jsonify(qualities)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        video_url = data.get('url')
        itag = data.get('itag')
        if not video_url or not itag:
            return jsonify({"error": "URL and quality selection are required"}), 400

        yt = YouTube(video_url)
        stream = yt.streams.get_by_itag(itag)
        filename = stream.download(output_path=DOWNLOAD_FOLDER)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
