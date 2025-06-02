import os
import re
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from pytube import YouTube
import whisper
import yt_dlp
from glob import glob

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def get_transcript_youtube(video_url,model_size="base"):
    video_id = extract_video_id(video_url)
    
    try:
        # Try YouTube transcript API
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        return " ".join([item['text'] for item in transcript])
    
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, Exception) as e:
        print(f"[INFO] Transcript not found, falling back to Whisper. Reason: {e}")

        # Download audio 
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_output_path = os.path.join(tmpdir, "audio.%(ext)s")

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_output_path,
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])

                # Find the downloaded file
                mp3_files = glob(os.path.join(tmpdir, "*.mp3"))
                if not mp3_files:
                    return "[ERROR] Audio download failed (no .mp3 found)."
                audio_file = mp3_files[0]

                # Transcribe using Whisper
                model = whisper.load_model(model_size)
                result = model.transcribe(audio_file)

                return result["text"]

        except Exception as e:
            return f"[ERROR] Failed to transcribe: {e}"
"""
video_url = "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
transcript_text = get_transcript_youtube(video_url)
print("Output of get_transcript_youtube","\n","\n")
print(transcript_text)
"""