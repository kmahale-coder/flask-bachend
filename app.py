from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # 👈 CORS enable karna mat bhoolo

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    quality = data.get('quality')

    if not url:
        return {"error": "No URL provided"}, 400

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': 'downloaded_video.mp4',  # 👈 MP4 format ensure karo
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file('downloaded_video.mp4', as_attachment=True, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
