from datetime import datetime
from typing import Optional, Sequence

from fastapi import APIRouter
from pydantic import BaseModel
from schedule import get_jobs, idle_seconds, run_all

from ...twitter.me import MeResponse, me

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)


class ScheduledTask(BaseModel):
    func: str
    last_run: Optional[datetime]
    next_run: Optional[datetime]


class TaskSummary(BaseModel):
    ahead_second: float
    tasks: Sequence[ScheduledTask]


class FlushTaskResponse(TaskSummary):
    flushed: bool


def get_task_summary() -> TaskSummary:
    tasks = [
        ScheduledTask(
            func=str(job.job_func),
            last_run=job.last_run,
            next_run=job.next_run,
        ) for job in get_jobs()
    ]
    res = TaskSummary(
        ahead_second=idle_seconds() or 0,
        tasks=tasks,
    )
    return res


@router.post('/flush')
def flush_tasks() -> TaskSummary:
    res = FlushTaskResponse(
        flushed=True,
        **get_task_summary().dict(),
    )
    run_all()
    return res


@router.get('/task')
def list_tasks() -> TaskSummary:
    res = get_task_summary()
    return res


@router.get('/me')
def show_user_info() -> MeResponse:
    return me().data
