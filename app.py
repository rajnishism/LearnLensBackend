from flask import Flask, jsonify, send_file, abort
import os

from Video import generate_pdf_from_youtube_video 
from Playlist import generate_playlist_summary # Your existing functions

app = Flask(__name__)

# Define where your PDFs will be stored


VIDEO_DIR = 'VideoSummary'
PLAYLIST_DIR = 'PlaylistSummary'

@app.route('/video/<video_id>')
def get_video_summary(video_id):
    try:
        pdf_path = f"VideoSummary/{video_id}.pdf"

        # Step 1: Check if file exists
        if not os.path.exists(pdf_path):
            print(f"PDF not found for {video_id}. Generating...")
            success = generate_pdf_from_youtube_video(video_id)
            if not success or not os.path.exists(pdf_path):
                return jsonify({"error": "Failed to generate summary"}), 400

        # Step 2: File exists — send it
        print(f"Sending file: {pdf_path}")
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

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
    port = int(os.environ.get('PORT', 6000))  # Get port from environment, fallback to 5000 for local testing
    app.run(host='0.0.0.0', port=5001)