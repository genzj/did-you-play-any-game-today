from pathlib import Path

from fastapi.testclient import TestClient
from requests_mock import Mocker


def test_task(client: TestClient):
    response = client.get('/api/admin/task')
    assert response.status_code == 200
    task = response.json()
    assert len(task['tasks']) > 0


def test_me(client: TestClient, requests_mock: Mocker, oauth_asserter):
    requests_mock.get(
        'https://api.twitter.com/2/users/me',
        json={
            'data': {
                'created_at': '2000-12-25T08:00:00.000Z',
                'id': 'test',
                'name': 'fake user',
                'profile_image_url': 'https://fake.com/a.png',
                'username': 'fake_user',
            }
        },
    )
    response = client.get('/api/admin/me')
    request = requests_mock.request_history[0]
    oauth_asserter(request)
    assert request.qs == {'user.fields': ['created_at,profile_image_url']}

    assert response.status_code == 200
    me = response.json()
    assert me['id'] == 'test'
    assert me['name'] == 'fake user'


def test_flush_without_state(
    client: TestClient,
    requests_mock: Mocker,
    oauth_asserter,
    state_file: Path
):
    state_file.unlink(missing_ok=True)
    requests_mock.post(
        'https://api.twitter.com/2/tweets',
        status_code=201,
        json={
            'data': {
                'edit_history_tweet_ids': ['1234'],
                'id': '1234',
                'text': 'text',
            }
        },
    )
    response = client.post('/api/admin/flush')
    request = requests_mock.request_history[0]
    oauth_asserter(request)
    assert request.json() == {'text': 'no'}

    assert response.status_code == 200
    flush = response.json()
    assert len(flush['tasks']) > 0


def test_flush_with_state(
    client: TestClient,
    requests_mock: Mocker,
    oauth_asserter,
    state_file: Path
):
    state_file.unlink(missing_ok=True)
    # submit a play info
    response = client.post('/api/game/play')
    assert response.is_success
    assert state_file.is_file()

    requests_mock.post(
        'https://api.twitter.com/2/tweets',
        status_code=201,
        json={
            'data': {
                'edit_history_tweet_ids': ['1234'],
                'id': '1234',
                'text': 'text',
            }
        },
    )
    response = client.post('/api/admin/flush')
    request = requests_mock.request_history[0]
    oauth_asserter(request)
    assert request.json() == {'text': 'yes'}

    assert response.status_code == 200
    flush = response.json()
    assert len(flush['tasks']) > 0

    assert not state_file.exists()
