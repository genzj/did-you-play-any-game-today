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
