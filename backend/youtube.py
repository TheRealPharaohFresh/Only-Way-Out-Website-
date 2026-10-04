import os

import requests
from flask import Blueprint, jsonify, request

youtube_bp = Blueprint("youtube", __name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Map your tracks to actual YouTube video IDs
TRACK_TO_VIDEO_ID = {
    "keep-it-100": "Fuw5aC425bg",
    "for-me": "TjfAwgru-JU",
}


@youtube_bp.route("/youtube_views")
def youtube_views():
    if not YOUTUBE_API_KEY:
        return jsonify({"error": "YouTube API key is not configured"}), 503

    track = request.args.get("track")
    video_id = TRACK_TO_VIDEO_ID.get(track)

    if not video_id:
        return jsonify({"error": "Invalid track ID"}), 400

    url = (
        "https://www.googleapis.com/youtube/v3/videos?part=statistics"
        f"&id={video_id}&key={YOUTUBE_API_KEY}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return jsonify({"error": "YouTube data fetch failed"}), 502

    data = response.json()
    if "items" not in data or not data["items"]:
        return jsonify({"error": "YouTube data fetch failed"}), 502

    views = data["items"][0]["statistics"]["viewCount"]
    view_count = int(views)
    if view_count < 100:
        return jsonify({"youtube_views": None, "views_hidden": True})

    return jsonify({"youtube_views": view_count, "views_hidden": False})
