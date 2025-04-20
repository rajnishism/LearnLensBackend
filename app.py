from flask import Flask, send_file, abort
import os
from flask_cors import CORS
from Video import generate_pdf_from_youtube_video 
from Playlist import generate_playlist_summary # Your existing functions

app = Flask(__name__)
CORS(app)  # 🔥 Enables CORS for all routes
# Define where your PDFs will be stored


VIDEO_DIR = 'VideoSummary'
PLAYLIST_DIR = 'PlaylistSummary'

@app.route('/video/<video_id>')
def get_video_summary(video_id):
    pdf_path = os.path.join(VIDEO_DIR, f"{video_id}.pdf")
    print(pdf_path)
    
    # If it doesn't exist, generate it
    if not os.path.exists(pdf_path):
        success = generate_pdf_from_youtube_video(video_id)
        if not success:
            abort(500, description="Failed to generate video summary")
    
    return send_file(pdf_path, as_attachment=True)

@app.route('/playlist/<playlist_id>')
def get_playlist_summary(playlist_id):
    pdf_path = os.path.join(PLAYLIST_DIR, f"{playlist_id}.pdf")
    
    # If it doesn't exist, generate it
    if not os.path.exists(pdf_path):
        success = generate_playlist_summary(playlist_id)
        if not success:
            abort(500, description="Failed to generate playlist summary")

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
