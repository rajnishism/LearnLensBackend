import subprocess
import os

def get_transcript_from_youtube(video_id):
    filename = f"{video_id}.en.vtt"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        # Run yt-dlp to download auto-generated subtitles
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "-o", f"{video_id}.%(ext)s",
            url
        ], check=True)

        # Read the subtitle file
        transcript = ""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    if "-->" not in line and line.strip() and not line.strip().isdigit():
                        transcript += line.strip() + " "

            # Optionally, clean up the file
            os.remove(filename)

        return transcript

    except subprocess.CalledProcessError as e:
        print(f"yt-dlp error: {e}")
        return "Transcript fetch failed."
