# -------------------------------
# Stage 1: Builder
# -------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (optimizes layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# -------------------------------
# Stage 2: Runtime
# -------------------------------
FROM python:3.12-slim

ENV TZ=UTC
WORKDIR /app

# Install system dependencies (cron, timezone tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

# Copy installed modules from builder stage
COPY --from=builder /usr/local/lib/python3.12/ /usr/local/lib/python3.12/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy FastAPI source code
COPY app /app/app
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem

# -------------------------------
# Cron Setup
# -------------------------------
# Create required directories
RUN mkdir -p /data && \
    mkdir -p /cron && \
    chmod 755 /data /cron

# Copy cron script
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Permissions for cron file
RUN chmod 0644 /etc/cron.d/2fa-cron

# Apply cron job
RUN crontab /etc/cron.d/2fa-cron

# -------------------------------
# Expose API port
# -------------------------------
EXPOSE 8080

# -------------------------------
# Start cron + FastAPI app
# -------------------------------
CMD service cron start && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080
