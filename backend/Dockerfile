# Base image using official Python slim
FROM python:3.10-slim as builder

# Setup build dependencies and environment
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim
WORKDIR /app

# Copy python dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy backend files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
