#!/usr/bin/env bash
set -e

IMAGE_NAME="spreadsheetscape"
CONTAINER_NAME="spreadsheetscape"

docker build -t "$IMAGE_NAME" . 

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

docker run -d \
    --name "$CONTAINER_NAME" \
    -p 5000:5000 \
    -p 8765:8765 \
    "$IMAGE_NAME"

echo "SheetScape läuft auf:"
echo "  http://localhost:5000"
echo "TTS läuft auf:"
echo "  http://localhost:8765"
