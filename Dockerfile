# Use a base image with Python 3 already installed
FROM python:3.9.13

# Install system dependencies for Redis
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Start redis server
RUN redis-server --daemonize yes

# Set the working directory
WORKDIR /usr/src/app

# Copy only the requirements file first
COPY requirements.txt ./

# Install dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

RUN pip uninstall httpcore -y
RUN pip uninstall httpx -y
RUN pip install httpcore
RUN pip install httpx
RUN pip install redis

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run your application
ENTRYPOINT ["sh", "-c", "redis-server --daemonize yes && alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 8000"]
