FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if any are needed
# (Using python urllib.request for healthcheck, so no curl/wget needed)

# Copy and install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose port
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
