import hashlib
import hmac
import os
import time
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://onlywayout.netlify.app,http://localhost:3000,http://localhost:5000,http://127.0.0.1:5500,http://127.0.0.1:3000",
).split(",")
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

# Register YouTube blueprint
try:
    from .youtube import youtube_bp
except ImportError:  # pragma: no cover - supports running this file directly
    from youtube import youtube_bp

app.register_blueprint(youtube_bp, url_prefix="/api/youtube")

# Load environment variables
DOWNLOAD_TOKEN = os.getenv("SECRET_TOKEN")
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
MUSIC_DIR = FRONTEND_DIR / "Music"
TRACK_MAP = {
    "keep-it-100": "PharaohFresh Ft AtlJacob - Keep It 100.mp3",
    "for-me": "PharaohFresh-For Me.mp3",
}


def _build_signed_token(track: str, expires_at: int) -> str:
    if not DOWNLOAD_TOKEN:
        raise RuntimeError("Server is missing SECRET_TOKEN")
    payload = f"{track}:{expires_at}".encode("utf-8")
    digest = hmac.new(DOWNLOAD_TOKEN.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return f"{expires_at}.{digest}"


def _verify_signed_token(track: str, token: str) -> bool:
    if not DOWNLOAD_TOKEN:
        return False
    try:
        expires_at_raw, digest = token.split(".", 1)
        expires_at = int(expires_at_raw)
    except (ValueError, TypeError):
        return False

    if expires_at < time.time():
        return False

    expected = hmac.new(
        DOWNLOAD_TOKEN.encode("utf-8"),
        f"{track}:{expires_at}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(digest, expected)


@app.route("/", methods=["GET"])
def index():
    return jsonify(message="🔥 Welcome to Pharaoh's Secure Download API")


@app.route("/api/download-url/<track>", methods=["GET"])
def signed_download_url(track):
    if not DOWNLOAD_TOKEN:
        abort(500, description="Server is missing SECRET_TOKEN")

    track_key = track.lower()
    if track_key not in TRACK_MAP:
        abort(404, description="Track not found")

    expires_at = int(time.time()) + 300
    signed_token = _build_signed_token(track_key, expires_at)
    download_url = f"{request.url_root.rstrip('/')}/download/{track_key}?token={signed_token}"
    return jsonify({"download_url": download_url})


@app.route("/download/<track>")
def download(track):
    token = request.args.get("token")

    if not DOWNLOAD_TOKEN:
        abort(500, description="Server is missing SECRET_TOKEN")

    if not token or not _verify_signed_token(track.lower(), token):
        abort(403, description="Unauthorized or missing token")

    filename = TRACK_MAP.get(track.lower())
    if not filename:
        abort(404, description="Track not found")

    file_path = (MUSIC_DIR / filename).resolve()
    allowed_root = MUSIC_DIR.resolve()

    try:
        file_path.relative_to(allowed_root)
    except ValueError:
        abort(404, description="Track not found")

    if not file_path.is_file():
        abort(404, description="File missing on server")

    return send_file(file_path, as_attachment=True, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=False)
