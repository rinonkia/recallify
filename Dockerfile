FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY src ./src

# Install dependencies using uv
RUN uv sync

# Keep container running
CMD ["tail", "-f", "/dev/null"]
