import requests

def get_video_ids_from_playlist(playlist_id, api_key):
    video_ids = []
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }

    while True:
        response = requests.get(base_url, params=params).json()
        for item in response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])
        if "nextPageToken" in response:
            params["pageToken"] = response["nextPageToken"]
        else:
            break

    return video_ids

# Usage
API_KEY = "AIzaSyBaNlWbmPkJW02RDcpszdwYMM3LtZNGGE0"
PLAYLIST_ID = "PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0"
# video_ids = get_video_ids_from_playlist(PLAYLIST_ID, API_KEY)

