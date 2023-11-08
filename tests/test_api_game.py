from fastapi.testclient import TestClient
from pathlib import Path


def test_no_play(client: TestClient, state_file: Path):
    state_file.unlink(missing_ok=True)
    response = client.get('/api/game/play')
    assert response.is_success
    play = response.json()
    assert not play['played']
    assert play['timestamp'] == 0.0


def test_submit_play(client: TestClient, state_file: Path):
    state_file.unlink(missing_ok=True)

    # submit a play info
    response = client.post('/api/game/play')
    assert response.is_success
    play = response.json()
    assert play['played']
    assert play['timestamp'] > 0.0
    ts = play['timestamp']

    # read it back
    response = client.get('/api/game/play')
    assert response.is_success
    play = response.json()
    assert play['played']
    assert play['timestamp'] == ts
