from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ...config import settings

router = APIRouter(
    prefix='/game',
    tags=['game'],
)


def timestamp_now() -> float:
    return datetime.now(timezone.utc).timestamp()


class GamePlay(BaseModel):
    timestamp: float = Field(
        default_factory=timestamp_now,
    )
    played: bool = False


@router.post('/play')
async def record_play() -> GamePlay:
    play = GamePlay(played=True)
    with open(
        settings.get('state_file_path', '.state.json'),
        'w'
    ) as state:
        state.write(play.json())
    return play


@router.get('/play')
async def list_play() -> GamePlay:
    try:
        state = settings.get('state_file_path', '.state.json')
        play = GamePlay.parse_file(state)
    except Exception:
        play = GamePlay(timestamp=0)
    return play
