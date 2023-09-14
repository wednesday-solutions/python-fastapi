# Use a base image with Python 3 already installed
FROM python:3

# Set the working directory
WORKDIR /usr/src/app

# Copy only the requirements file first
COPY requirements.txt ./

# Install dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run your application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 8000"]
