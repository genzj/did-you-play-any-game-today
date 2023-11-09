import os
import tempfile
from pathlib import Path

from nox import Session, session

os.environ.update({
    "PDM_IGNORE_SAVED_PYTHON": "1",
    "PDM_NO_LOCK": "1",
})

python_versions = ['3.11', '3.10', '3.12']
main_python_version = python_versions[0]


@session(python=python_versions)
def test(session: Session):
    """Run pytest UT"""
    session.run_always('pdm', 'install', '-G', 'test', external=True)
    try:
        session.run(
            'coverage',
            'run',
            '--parallel-mode',
            '-m',
            'pytest',
            *session.posargs
        )
    finally:
        if session.interactive:
            session.notify('coverage', posargs=[])


@session(python=python_versions)
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]
    session.run_always('pdm', 'install', '-G', 'test', external=True)

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=main_python_version)
def safety(session: Session):
    """Scan dependencies for insecure packages."""
    session.run_always('pdm', 'install', '-G', 'lint', external=True)
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "pdm",
            "list",
            "--freeze",
            external=True,
            stdout=requirements,
        )
        session.run(
            "safety",
            "check",
            "--full-report",
            f"--file={requirements.name}"
        )


@session(python=main_python_version)
def bandit(session: Session):
    """Scan security issues"""
    session.run_always('pdm', 'install', '-G', 'lint', external=True)
    session.run(
        "bandit",
        "-r",
        "src/did_you_play_any_game_today"
    )
