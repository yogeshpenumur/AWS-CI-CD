#!/bin/bash

set -e

IMAGE_NAME="yogeshpenumur/simple-python-flask-app"

echo "Looking for containers running image: $IMAGE_NAME"

# Find container ID(s) using the image
CONTAINER_IDS=$(docker ps -a --filter "ancestor=$IMAGE_NAME" --format "{{.ID}}")

if [ -n "$CONTAINER_IDS" ]; then
  echo "Stopping and removing the following container(s):"
  echo "$CONTAINER_IDS"

  # Stop containers (if running)
  docker stop $CONTAINER_IDS || true

  # Remove containers
  docker rm $CONTAINER_IDS
else
  echo "No containers found running image: $IMAGE_NAME"
fi
