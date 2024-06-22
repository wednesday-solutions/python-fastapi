FROM python:3.11.8-slim as base
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    nonroot
# Install all OS dependencies for fully functional requirements.txt install
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the python base image may be rebuilt too seldom sometimes (less than once a month)
    # required for psutil python package to install
    python3-dev \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
#initiallizing opentelemetry to monitor app
RUN opentelemetry-bootstrap --action=install

# # Download the time freeze agent
ADD https://keploy-enterprise.s3.us-west-2.amazonaws.com/releases/latest/assets/freeze_time_arm64.so /lib/keploy/freeze_time_arm64.so

# Set LD_PRELOAD environment variable to use freeze_time_arm64.so
ENV LD_PRELOAD=/lib/keploy/freeze_time_arm64.so

# Switch to the non-privileged user to run the application.
# USER nonroot

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000
# Run the application.
# CMD ["sh", "-c", "alembic upgrade head && opentelemetry-instrument uvicorn app.app:app --host 0.0.0.0 --port 8000"]
CMD ["python3", "-m", "coverage", "run", "-p", "-m", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
