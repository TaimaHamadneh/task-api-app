# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final image
FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH to include local Python packages
ENV PATH=/root/.local/bin:$PATH

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Copy application code
COPY . .

# Default command
CMD ["flask", "run", "--host=0.0.0.0"]