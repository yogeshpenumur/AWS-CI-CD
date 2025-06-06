
#!/bin/bash
set -e

# Define the container nameyogeshpenumur/simple-python-flask-app
CONTAINER_NAME=yogeshpenumur/simple-python-flask-app

# Check if the container is running
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
  echo "Stopping and removing running container: $CONTAINER_NAME"
  docker rm -f "$CONTAINER_NAME"
else
  echo "No running container named $CONTAINER_NAME found."
fi
