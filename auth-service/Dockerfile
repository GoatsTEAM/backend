FROM python:3.12-slim

ARG USER=appuser
ARG UID=1000
ARG GID=1000

RUN addgroup --gid $GID $USER && adduser --disabled-password --gecos '' --uid $UID --gid $GID $USER

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential gcc python3-dev tree

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

ENV UV_HTTP_TIMEOUT=60
RUN uv venv && uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY app/ ./

COPY entrypoint.sh ./

RUN chown -R $UID:$GID /app

USER $USER

RUN chmod +x ./entrypoint.sh

EXPOSE ${REST_PORT}
EXPOSE ${GRPC_PORT}

ENV PYTHONPATH=/app:/app/app_src

#CMD cd ../ && ls -al app 
ENTRYPOINT ["./entrypoint.sh"]
