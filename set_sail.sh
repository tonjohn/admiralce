#!/bin/bash
echo "[AdmiralCE] Stopping container..."
docker stop monsoor

echo "[AdmiralCE] Building image..."
docker build -t zumwalt .

echo "[AdmiralCE] Starting container..."
docker run --rm -d -p 8000:8000 --name monsoor zumwalt

echo "[AdmiralCE] Launching Chrome..."
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome http://localhost:8000