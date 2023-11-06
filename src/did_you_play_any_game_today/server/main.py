from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .routers import admin, game
from .task import scheduled_tasks


@asynccontextmanager
async def lifespan(_: FastAPI):
    await scheduled_tasks()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(admin.router, prefix='/api')
app.include_router(game.router, prefix='/api')


@app.get("/")
async def redirect_to_ui():
    return RedirectResponse(url="/index.html")

app.mount("/", StaticFiles(directory="static"), name="ui")
