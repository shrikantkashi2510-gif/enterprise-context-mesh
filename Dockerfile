# Use a slim Python 2026-grade image
FROM python:3.12-slim-bookworm

# Security: Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for asyncpg (Postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Security: Create a non-root user and switch to it
RUN useradd -m mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose port (if using SSE transport, otherwise stdio uses stdin/out)
EXPOSE 8000

# Entrypoint for the MCP Server
CMD ["python", "main.py"]
