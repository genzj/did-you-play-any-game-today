from pathlib import Path

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from schedule import every, repeat, run_pending

from ..config import settings
from ..twitter import send_text_tweet
from .routers import admin, game

app = FastAPI()
app.include_router(admin.router)
app.include_router(game.router)


@app.on_event('startup')
@repeat_every(seconds=60)
def scheduled_tasks() -> None:
    run_pending()


@repeat(every().day.at(
    settings.get('tweet_at', '04:44'),
    settings.get('tweet_at_timezone', 'America/Vancouver')
))
def tweet():
    state = Path(
        settings.get('state_file_path', '.state.json')
    )
    if state.is_file():
        send_text_tweet(
            settings.get('positive_tweet', '🎊 Yes! 🎉')
        )
        state.unlink()
    else:
        send_text_tweet(
            settings.get('negative_tweet', 'No...🥲')
        )
