FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# System deps + kreuzberg runtime (PDF extraction)
RUN apt-get update && apt-get install -y \
    curl git build-essential ca-certificates \
    software-properties-common \
    libgl1 poppler-utils tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y \
    python3.12 python3.12-dev python3.12-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# uv (installed system-wide)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# Node 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Non-root user (VS Code devcontainer convention)
# ubuntu:24.04 ships with a 'ubuntu' user at UID 1000 — remove it first
RUN userdel -r ubuntu 2>/dev/null || true && \
    useradd -m -s /bin/bash -u 1000 vscode
USER vscode
WORKDIR /workspace
