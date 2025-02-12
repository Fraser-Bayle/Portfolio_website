# Stage 1: Builder - Install dependencies and run tests
FROM python:3.13-slim AS builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (e.g., gcc, libpq-dev for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies into wheels directory
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r requirements.txt

# Copy the rest of the code
COPY . .

# (Optional) Run tests and lint checks in this stage to catch issues early
# RUN pytest --maxfail=1 --disable-warnings -q
# RUN flake8 .

# Stage 2: Final image
FROM python:3.13-slim

# Create non-root user for security
RUN addgroup --system app && adduser --system --group app

# Set work directory and environment variables
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy installed wheels from the builder stage and install them
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the Django application code
COPY . $APP_HOME

# Change ownership to the non-root user
RUN chown -R app:app $APP_HOME

# Copy and prepare the production entrypoint script
COPY entrypoint.prod.sh .
RUN sed -i 's/\r$//g' entrypoint.prod.sh && chmod +x entrypoint.prod.sh

# Switch to non-root user
USER app

# Expose port 8000 (internal, not published here)
EXPOSE 8000

# Set entrypoint to run migrations, collect static files, and start Gunicorn
ENTRYPOINT ["./entrypoint.prod.sh"]
