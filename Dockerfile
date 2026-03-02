FROM ghcr.io/astral-sh/uv:alpine3.23 AS build

WORKDIR /app

RUN apk add build-base clang-dev patchelf

RUN uv python install 3.13

COPY pyproject.toml uv.lock .python-version .

RUN uv sync --locked

COPY . .

RUN uv run nuitka --mode=standalone --follow-imports --clang --assume-yes-for-downloads --output-filename=sunborne --output-dir=publish --include-package-data=emoji main.py

FROM alpine:3.23 AS pack

WORKDIR /app

COPY --from=build /app/publish/main.dist/ .

ENTRYPOINT [ ]

CMD [ "./sunborne" ]