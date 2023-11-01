from schedule import every, repeat, run_pending
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from ..config import settings
from .routers import game


app = FastAPI()
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
    # Run tweet sending process
    pass
