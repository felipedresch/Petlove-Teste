# Stage de build
FROM python:3.11-slim AS builder

# Instalar dependências
RUN apt-get update && apt-get install -y curl gcc && rm -rf /var/lib/apt/lists/*

# Instalar uv e adicionar ao PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && mv /root/.local/bin/uv /usr/local/bin/uv && mv /root/.local/bin/uvx /usr/local/bin/uvx

WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv sync --frozen --no-dev

COPY . .

# Stage de produção
FROM python:3.11-slim AS runner
RUN apt-get update && apt-get install -y dumb-init && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# usuário não-root
RUN addgroup --system --gid 1001 appuser && adduser --system --uid 1001 --gid 1001 appuser

# Copiar ambiente virtual e código do stage de build
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app /app

# diretório de logs com permissões corretas
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

USER appuser
EXPOSE 3000

# dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "4"]

