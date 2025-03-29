from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        video_url = data.get("url")
        
        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        yt = YouTube(video_url)
        
        # ✅ Best Video Stream
        video_stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by("resolution").desc().first()
        # ✅ Best Audio Stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        if not video_stream or not audio_stream:
            return jsonify({"error": "No valid video/audio streams found"}), 400

        # ✅ Download Files
        video_path = video_stream.download(filename="video.mp4")
        audio_path = audio_stream.download(filename="audio.mp4")

        # ✅ Merge Video + Audio
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        final_clip = video_clip.set_audio(audio_clip)
        final_video_path = "final_video.mp4"
        final_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

        # ✅ Cleanup (Delete Temp Files)
        os.remove(video_path)
        os.remove(audio_path)

        return send_file(final_video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
