import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Set up your proxy (replace with a valid one)
proxies = {
    'http': 'http://35.154.71.72',
    'https': 'http://15.206.25.41',
}

# Monkey patch requests.get to always use proxy
original_get = requests.get

def proxy_get(*args, **kwargs):
    kwargs['proxies'] = proxies
    return original_get(*args, **kwargs)

requests.get = proxy_get  # Apply monkey patch

# Your transcript fetch function
def get_transcript_from_youtube(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        result = ytt_api.fetch(video_id, ['en', 'hi'])
        transcript = ""
        for snippet in result:
            transcript += snippet['text']
        return transcript
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        return ""

requests.get = original_get  # Restore original requests.get after use
