from fastapi.testclient import TestClient

from did_you_play_any_game_today.server.routers.admin import TaskSummary


def test_task(client: TestClient):
    response = client.get('/api/admin/task')
    assert response.status_code == 200
    task: TaskSummary = TaskSummary(**response.json())
    assert len(task.tasks) > 0
