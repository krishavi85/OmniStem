FROM python:3.11-slim

ARG OMNISTEM_EXTRAS=demucs

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir ".[${OMNISTEM_EXTRAS}]"

ENTRYPOINT ["omnistem"]
CMD ["--help"]
