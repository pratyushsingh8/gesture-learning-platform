# Overwrite Dockerfile with the recommended CI-friendly content
@'
# Dockerfile - headless OpenCV + Flask (CI-friendly)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install a few system deps often needed for ML/OpenCV packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

# Default command to run the Flask app
CMD ["python", "app.py"]
'@ | Set-Content -Path Dockerfile -Encoding utf8

# Stage the resolved file
git add Dockerfile

# Continue the rebase
git rebase --continue

# If rebase finishes successfully, push your branch to remote
git push origin main
