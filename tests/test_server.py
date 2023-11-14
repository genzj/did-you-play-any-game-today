from unittest.mock import patch

from fastapi.testclient import TestClient


def test_redirect_to_ui(client: TestClient):
    response = client.get('')
    assert response.status_code == 307
    assert response.headers['Location'] == '/index.html'


def test_scheduled_task_start(client: TestClient):
    with patch(
        'did_you_play_any_game_today.server.task.run_pending'
    ) as mock_run_pending:
        mock_run_pending.assert_not_called()
        # https://www.starlette.io/lifespan/#running-lifespan-in-tests
        # the lifespan should be called after entering next context
        with client:
            pass
        # lifespan called the scheduled task, which in turn called the
        # run_pending because it's scheduled with wait_first == False
        mock_run_pending.assert_called_once()


def test_scheduled_task_period(client: TestClient):
    with patch(
        'did_you_play_any_game_today.server.task.run_pending'
    ) as mock_run_pending, patch(
        'fastapi_utils.tasks.asyncio.sleep'
    ) as mock_async_sleep:
        mock_run_pending.assert_not_called()
        # https://www.starlette.io/lifespan/#running-lifespan-in-tests
        # the lifespan should be called after entering next context
        with client:
            pass
        mock_async_sleep.assert_awaited()
        # after mocking the sleep, the run_pending should be
        # called multiple times at a very fast speed
        mock_run_pending.assert_called()
        assert mock_run_pending.call_count >= 2
