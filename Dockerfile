# syntax=docker/dockerfile:1

# https://pdm.fming.dev/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile

ARG PYTHON_VERSION=3.11.6

FROM python:${PYTHON_VERSION} as builder
ARG PROJECT=did_you_play_any_game_today

# install PDM
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip setuptools wheel pdm

# copy files
COPY pyproject.toml pdm.lock README.md /${PROJECT}/
COPY src/ /${PROJECT}/src

# install dependencies and project into the local packages directory
WORKDIR /${PROJECT}
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


# run stage
FROM python:${PYTHON_VERSION}-slim
ARG PROJECT=did_you_play_any_game_today
ARG PYTHON_SHORT_VERSION=3.11

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
WORKDIR /${PROJECT}

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

# retrieve packages from build stage
ENV PYTHONPATH=/${PROJECT}/pkgs
COPY --from=builder /${PROJECT}/__pypackages__/${PYTHON_SHORT_VERSION}/lib /${PROJECT}/pkgs

# retrieve executables
COPY --from=builder /${PROJECT}/__pypackages__/${PYTHON_SHORT_VERSION}/bin/* /bin/

# set command/entrypoint, adapt to fit your needs
# CMD ["python", "-m", "did_you_play_any_game_today"]
CMD ["uvicorn", "did_you_play_any_game_today.server.main:app"]
