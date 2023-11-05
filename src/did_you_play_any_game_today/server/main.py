from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from schedule import every, repeat, run_pending

from ..config import settings
from ..twitter import send_text_tweet
from .routers import admin, game

app = FastAPI()
app.include_router(admin.router, prefix='/api')
app.include_router(game.router, prefix='/api')


@app.get("/")
async def redirect_to_ui():
    return RedirectResponse(url="/index.html")

app.mount("/", StaticFiles(directory="static"), name="ui")


@app.on_event('startup')
@repeat_every(seconds=60)
def scheduled_tasks() -> None:
    run_pending()


@repeat(every().day.at(
    settings.tweet_at,
    settings.tweet_at_timezone,
))
def tweet():
    state = Path(settings.state_file_path)
    if state.is_file():
        send_text_tweet(settings.positive_tweet)
        state.unlink()
    else:
        send_text_tweet(settings.negative_tweet)
