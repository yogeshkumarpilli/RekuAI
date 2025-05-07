FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    VIRTUAL_ENV=/app/.venv \
    PATH="/root/.local/bin:/app/.venv/bin:$PATH" 

# Install system dependencies required by TensorFlow
RUN apt-get update && apt-get install -y  && apt-get install -y curl\
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

# -----------------------------------------------------------------------------
# Python Package Management Setup
# -----------------------------------------------------------------------------
# Install uv (modern Python dependency manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 

# Copy application code
COPY . .

# Create and set up virtual environment
RUN uv venv && \
    uv sync && \
    uv build

# Train the model before running the application
RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 80

# Command to run the app
CMD ["python", "application.py"]
