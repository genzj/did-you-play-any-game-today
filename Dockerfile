# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11.6

FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY ./ui/did-you-play-any-game-today/ /app
WORKDIR /app

FROM base AS uibuild
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

# https://pdm.fming.dev/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile
FROM python:${PYTHON_VERSION} as apibuilder
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
WORKDIR /${PROJECT}

# retrieve UI files
COPY --from=uibuild /app/dist static

# retrieve packages from build stage
ENV PYTHONPATH=/${PROJECT}/pkgs
COPY --from=apibuilder /${PROJECT}/__pypackages__/${PYTHON_SHORT_VERSION}/lib /${PROJECT}/pkgs

# retrieve executables
COPY --from=apibuilder /${PROJECT}/__pypackages__/${PYTHON_SHORT_VERSION}/bin/* /bin/

# set command/entrypoint, adapt to fit your needs
# CMD ["python", "-m", "did_you_play_any_game_today"]
CMD ["uvicorn", "--host", "0.0.0.0", "did_you_play_any_game_today.server.main:app"]
