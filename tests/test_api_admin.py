from fastapi.testclient import TestClient


def test_task(client: TestClient):
    response = client.get('/api/admin/task')
    assert response.status_code == 200
    task = response.json()
    assert len(task['tasks']) > 0
