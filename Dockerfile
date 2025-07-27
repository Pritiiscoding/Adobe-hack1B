# Use Python 3.10 slim image for smaller size
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts
COPY extract_outline.py .
COPY pdf_analyzer.py .

# Set the entrypoint
ENTRYPOINT ["python", "extract_outline.py"]

# Default command (can be overridden when running the container)
CMD ["--help"]