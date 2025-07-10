# Use the official Python image.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip wheel
RUN pip install --only-binary=:all: PyYAML==5.4.1
RUN pip install -r requirements.txt

# Copy project files
COPY backend /app/backend

# Expose port (Cloud Run expects 8080)
EXPOSE 8080

# Start FastAPI with Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"] 