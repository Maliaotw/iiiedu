# 使用官方 Python 3.12 slim 映像檔作為基礎
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# 安裝編譯 uwsgi 所需的系統套件
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 先複製依賴定義
COPY pyproject.toml ./

# 安裝依賴（不包含開發套件）
RUN uv sync --no-dev --no-install-project

# 手動安裝 uwsgi (因為它不支援 Windows，所以不放進 pyproject.toml 以免本地開發報錯)
RUN uv pip install uwsgi>=2.0.21

# 最終執行階段
FROM python:3.12-slim

WORKDIR /app

# 複製 uv 執行檔
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 複製虛擬環境
COPY --from=builder /app/.venv /app/.venv
COPY . .

# 設定路徑
ENV PATH="/app/.venv/bin:$PATH"

# 暴露埠號
EXPOSE 8001

# 啟動命令：收集靜態檔案並啟動 uWSGI
CMD ["sh", "-c", "uv run manage.py collectstatic --noinput && uwsgi --ini uwsgi.ini"]
