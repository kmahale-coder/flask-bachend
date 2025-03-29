from pytube import YouTube
from moviepy.editor import VideoFileClip

video_url = "YOUTUBE_VIDEO_URL"
yt = YouTube(video_url)

video_stream = yt.streams.filter(only_video=True, file_extension="mp4").first()
audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

video_file = video_stream.download(filename="video.mp4")
audio_file = audio_stream.download(filename="audio.mp4")

# Merge Video and Audio
video_clip = VideoFileClip(video_file)
audio_clip = VideoFileClip(audio_file).audio

final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")

@app.route('/streams', methods=['POST'])
def available_streams():
    try:
        data = request.json
        video_url = data.get('url')
        print("Received URL:", video_url)  # Debugging output
        if not video_url:
            return jsonify({"error": "URL is required"}), 400

        yt = YouTube(video_url)
        streams = [{"itag": stream.itag, "mime_type": stream.mime_type, "resolution": stream.resolution, "abr": stream.abr} for stream in yt.streams]
        
        print("Available Streams:", streams)  # Debugging output
        return jsonify({"streams": streams})

    except Exception as e:
        print("Error:", str(e))  # Debugging output
        return jsonify({"error": str(e)})
