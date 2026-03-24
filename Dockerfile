FROM ghcr.io/astral-sh/uv:alpine3.23

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN uv python install 3.13

COPY pyproject.toml uv.lock .python-version .

RUN uv sync --locked

COPY . .

CMD ["uv", "run", "main.py"]