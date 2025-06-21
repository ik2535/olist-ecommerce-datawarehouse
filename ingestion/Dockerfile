# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements (if any)
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ingestion script and any needed files
COPY . .

# Optional: Set default command (can be overridden in docker-compose)
CMD ["python", "erp_loader.py"]
