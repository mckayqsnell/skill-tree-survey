# syntax=docker/dockerfile:1.9
# Multi-stage build for the Skill Tree Survey backend (uv-managed FastAPI + SQLite).
# - builder: resolves the locked dependencies into /app/.venv (prod only)
# - dev:     adds dev deps + hot reload (targeted by docker-compose.yml locally)
# - runtime: slim, non-root production image (default target; pushed to GHCR)
ARG PYTHON_VERSION=3.13
ARG UV_VERSION=0.9.17

# ---- builder -------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder
# Pull just the uv binary from the official distroless uv image (keeps builder lean).
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0
WORKDIR /app

# 1) Dependency layer — cached unless uv.lock / pyproject.toml change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# 2) Project layer — copy source and install the project itself.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ---- dev -----------------------------------------------------------------
FROM builder AS dev
# Add dev dependencies (pytest, ruff, httpx) on top of the prod venv.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health', timeout=5).status == 200 else 1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---- runtime (default / production) --------------------------------------
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
# SQLite lives here; the named volume mounts over it at runtime. Non-root user must own it.
RUN mkdir -p /app/data && chown nonroot:nonroot /app/data
USER nonroot
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health', timeout=5).status == 200 else 1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
