
#!/bin/bash
set -e

# Define the container name
CONTAINER_NAME="myapp"

# Check if the container is running
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
  echo "Stopping and removing running container: $CONTAINER_NAME"
  docker rm -f "$CONTAINER_NAME"
else
  echo "No running container named $CONTAINER_NAME found."
fi
