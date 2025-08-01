from flask import Flask, request, send_file, abort
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DOWNLOAD_TOKEN = os.getenv("SECRET_TOKEN")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MUSIC_DIR = os.path.join(BASE_DIR, "Music")


@app.route("/", methods=["GET"])
def index():
    return "🔥 Welcome to Pharaoh's Secure Download API"

@app.route("/download/<track>")
def download(track):
    token = request.args.get("token")
    print(f"Received token: {token}")

    if token != DOWNLOAD_TOKEN:
        abort(403, description="Unauthorized or missing token")

    track_map = {
    "keep-it-100": "PharaohFresh-Keep it 100 Ft Atl Jacob.mp3",
    "for-me": "PharaohFresh-For Me.mp3"
}


    filename = track_map.get(track)
    if not filename:
        abort(404, description="Track not found")

    file_path = os.path.join(MUSIC_DIR, filename)
    print(f"Looking for file at: {file_path}")  # <--- moved here

    if not os.path.exists(file_path):
        abort(404, description="File missing on server")

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run()