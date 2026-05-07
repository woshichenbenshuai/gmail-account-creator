# ==============================================================================
# Gmail Creator Pro — Docker Development & Runtime Environment
# ==============================================================================
# Build:
#   docker build -t gmail-creator-pro .
#
# Run (interactive):
#   docker run -it --rm \
#     -v "$PWD/config_examples:/app/config_examples" \
#     -v "$PWD/data:/app/data" \
#     gmail-creator-pro
#
# Run (headless):
#   docker run -it --rm \
#     -e GMAIL_HEADLESS=1 \
#     -v "$PWD/config:/app/config" \
#     -v "$PWD/data:/app/data" \
#     gmail-creator-pro
# ==============================================================================

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# ── System dependencies ──────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── Chrome for Selenium ─────────────────────────────────────────────────
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ── Application ─────────────────────────────────────────────────────────
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .

# ── Volumes ─────────────────────────────────────────────────────────────
VOLUME ["/app/config", "/app/data", "/app/config_examples"]

# ── Runtime ─────────────────────────────────────────────────────────────
ENTRYPOINT ["python", "auto_gmail_creator.py"]
