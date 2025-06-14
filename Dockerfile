FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ADD . /app
WORKDIR /app

RUN uv sync

CMD ["uv", "run", "app.py"]