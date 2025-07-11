#!/bin/bash
set -e

IMAGE_NAME="yogeshpenumur/simple-python-flask-app"
CONTAINER_NAME="flask-app"
PORT=9888

# Stop and remove old container using the same name (if exists)
if docker ps -a --format '{{.Names}}' | grep -w "$CONTAINER_NAME" > /dev/null; then
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" || true
    docker rm "$CONTAINER_NAME" || true
fi

# Optional: Stop any container already using the same port
CONTAINER_ID=$(docker ps --filter "publish=$PORT" --format "{{.ID}}")
if [ -n "$CONTAINER_ID" ]; then
    echo "Port $PORT is already in use by container $CONTAINER_ID. Stopping it..."
    docker stop "$CONTAINER_ID"
    docker rm "$CONTAINER_ID"
fi

# Pull the latest image
echo "Pulling latest image: $IMAGE_NAME"
docker pull "$IMAGE_NAME"

# Run the new container
echo "Starting new container: $CONTAINER_NAME"  
docker run -d --name "$CONTAINER_NAME" -p $PORT:9888 "$IMAGE_NAME"
