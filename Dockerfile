# Use Python 3.11 slim image for faster builds and smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for common packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (for better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY src/ ./src/
COPY pyproject.toml .
COPY knowledge/ ./knowledge/

# Create outputs directory
RUN mkdir -p outputs

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose port for web interface
EXPOSE 8000

# Health check using Railway's health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "prd_generator.main"]
