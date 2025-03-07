# Use the Python 3.10 Debian base image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install build dependencies and required libraries
RUN apt-get update \
    && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose port 5000
EXPOSE 5000

# Define the command to run the application
CMD ["python", "./app.py"]

HEALTHCHECK --interval=50s --timeout=15s --start-period=30s --retries=3 \
  CMD curl -f http://172.19.37.84:5000/health || exit 1