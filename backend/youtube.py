import requests
from flask import Blueprint, request, jsonify
import os

youtube_bp = Blueprint('youtube', __name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Set this in your .env

# Map your tracks to actual YouTube video IDs
TRACK_TO_VIDEO_ID = {
    "keep-it-100": "Fuw5aC425bg",  # Replace with your real video ID
    "for-me": "TjfAwgru-JU"        # Replace with your real video ID
}

@youtube_bp.route('/youtube_views')
def youtube_views():
    track = request.args.get("track")
    video_id = TRACK_TO_VIDEO_ID.get(track)

    if not video_id:
        return jsonify({"error": "Invalid track ID"}), 400

    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data or not data["items"]:
        return jsonify({"error": "YouTube data fetch failed"}), 502

    views = data["items"][0]["statistics"]["viewCount"]
    return jsonify({"youtube_views": int(views)})

