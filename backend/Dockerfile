FROM python:3.13-slim AS builder

RUN apt-get update && \
  apt-get install -y --no-install-recommends build-essential libpq-dev curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
  apt-get install -y nodejs

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

RUN pip install --no-cache-dir --upgrade pyopenssl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /root_project

COPY uv.lock pyproject.toml ./
COPY . .

RUN uv venv /root_project/.venv
ENV PATH="/root_project/.venv/bin:$PATH"
RUN uv sync --frozen --no-dev

FROM python:3.13-slim

RUN apt-get update && \
  apt-get install -y --no-install-recommends libpq5 curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
  apt-get install -y nodejs

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

WORKDIR /root_project

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --from=builder /root_project /root_project
EXPOSE 8000
