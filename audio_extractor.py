import ffmpeg
import os

def extract_audio(video_path):
    """Videodan audio ajratib olib, MP3 formatida saqlaydi."""
    audio_path = video_path.replace(".mp4", ".mp3")
    
    try:
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path, format='mp3', audio_bitrate='192k')
        ffmpeg.run(stream, overwrite_output=True)
        return audio_path
    except Exception as e:
        print(f"Xatolik: {e}")
        return None
