# Dockerfile (Debian-slim based)
# Overwrite Dockerfile with the recommended CI-friendly content
@'
# Dockerfile - headless OpenCV + Flask (CI-friendly)
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install a few system deps often needed for ML/OpenCV packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy pip requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
'@ | Set-Content -Path Dockerfile -Encoding utf8

# Stage the resolved file
git add Dockerfile

# Continue the rebase
git rebase --continue

# If rebase finishes successfully, push your branch to remote
git push origin main
