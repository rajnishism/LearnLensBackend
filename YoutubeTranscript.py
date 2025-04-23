from youtube_transcript_api import YouTubeTranscriptApi
ytt_api = YouTubeTranscriptApi()
video_id="E0Hmnixke2g"

# is iterable
def get_transcript_from_youtube(video_id):
    result =ytt_api.fetch(video_id,['en', 'hi'])
    # print(result)
    transcript =""
    for snippet in result:
        transcript+=snippet.text
    return transcript


