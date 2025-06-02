def get_transcript_youtube(video_url, model_size="base"):
    video_id = extract_video_id(video_url)
    
    try:
        # Try YouTube transcript API
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        return [{"start": item["start"], "duration": item["duration"], "text": item["text"]} for item in transcript]
    
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, Exception) as e:
        print(f"[INFO] Transcript not found, falling back to Whisper. Reason: {e}")

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

                mp3_files = glob(os.path.join(tmpdir, "*.mp3"))
                if not mp3_files:
                    return "[ERROR] Audio download failed (no .mp3 found)."
                audio_file = mp3_files[0]

                model = whisper.load_model(model_size)
                result = model.transcribe(audio_file, verbose=False)

                # Return segments with timestamps
                return [
                    {"start": segment["start"], "end": segment["end"], "text": segment["text"]}
                    for segment in result["segments"]
                ]

        except Exception as e:
            return f"[ERROR] Failed to transcribe: {e}"
