#backend 

from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    quality = data.get('quality', '720p')

    if not video_url:
        return {"error": "No URL provided"}, 400

    options = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_name = ydl.prepare_filename(info).replace(".webm", ".mp4").replace(".mkv", ".mp4")

    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
