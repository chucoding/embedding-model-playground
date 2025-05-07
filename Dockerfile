# Use Python 3.11 image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy source code
COPY . .

# Set port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "server.py", "--server.port=8501", "--server.address=0.0.0.0"]
