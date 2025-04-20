from YoutubePlaylist import get_video_ids_from_playlist
from Video import generate_pdf_from_youtube_video
from pypdf import PdfMerger
from dotenv import load_dotenv
from mergePdf import merge_pdfs
load_dotenv()
import os

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

def generate_playlist_summary(playlist_id):
        
        video_ids = get_video_ids_from_playlist(playlist_id, GOOGLE_API_KEY)
        filenames=[]
        print("Number of Videos in the playlist")
        print(len(video_ids))

        lectureNo=1
        for video_id in video_ids:
            
            generate_pdf_from_youtube_video(video_id, lectureNo)
            filenames.append("VideoSummary/"+video_id+".pdf")  # adding .pdf to video_ids fetched to match with the filename of the pdfs 
            lectureNo+=1
        merge_pdfs(filenames, playlist_id)

# Example Usage
#generate_playlist_summary("PLKnIA16_RmvbA_hYXlRgdCg9bn8ZQK2z9")