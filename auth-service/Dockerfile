FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential gcc python3-dev

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

ENV UV_HTTP_TIMEOUT=60
RUN uv venv && uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


EXPOSE ${REST_PORT}
EXPOSE ${GRPC_PORT}

ENV PYTHONPATH=/app/src
ENTRYPOINT ["/app/entrypoint.sh"]
