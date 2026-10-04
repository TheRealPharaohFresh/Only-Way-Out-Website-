import os
import time

os.environ.setdefault('SECRET_TOKEN', 'test-secret')

import pytest

import backend.app as app_module
import backend.youtube as youtube_module


@pytest.fixture
def client():
    app_module.app.config['TESTING'] = True
    with app_module.app.test_client() as client:
        yield client


def test_signed_download_url_returns_token(client):
    response = client.get('/api/download-url/keep-it-100')
    assert response.status_code == 200
    payload = response.get_json()
    assert 'download_url' in payload
    assert '/download/keep-it-100?token=' in payload['download_url']


def test_missing_token_denied(client):
    response = client.get('/download/keep-it-100')
    assert response.status_code == 403


def test_invalid_token_denied(client):
    response = client.get('/download/keep-it-100?token=not-a-valid-token')
    assert response.status_code == 403


def test_expired_token_denied(client):
    expired_token = app_module._build_signed_token('keep-it-100', int(time.time()) - 5)
    response = client.get(f'/download/keep-it-100?token={expired_token}')
    assert response.status_code == 403


def test_valid_token_download_succeeds(client):
    valid_token = app_module._build_signed_token('keep-it-100', int(time.time()) + 300)
    response = client.get(f'/download/keep-it-100?token={valid_token}')
    assert response.status_code == 200
    assert response.mimetype == 'audio/mpeg'


@pytest.mark.parametrize(
    ('view_count', 'expected_count', 'views_hidden'),
    [
        (99, None, True),
        (100, 100, False),
        (125, 125, False),
    ],
)
def test_youtube_view_count_threshold(
    client, monkeypatch, view_count, expected_count, views_hidden
):
    class YouTubeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                'items': [
                    {'statistics': {'viewCount': str(view_count)}}
                ]
            }

    monkeypatch.setattr(youtube_module, 'YOUTUBE_API_KEY', 'test-api-key')
    monkeypatch.setattr(
        youtube_module.requests, 'get', lambda *args, **kwargs: YouTubeResponse()
    )

    response = client.get('/api/youtube/youtube_views?track=keep-it-100')
    assert response.status_code == 200
    assert response.get_json() == {
        'youtube_views': expected_count,
        'views_hidden': views_hidden,
    }
