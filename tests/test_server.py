from fastapi.testclient import TestClient


def test_redirect_to_ui(client: TestClient):
    response = client.get('')
    assert response.status_code == 307
    assert response.headers['Location'] == '/index.html'
