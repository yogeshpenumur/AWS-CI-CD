#!/bin/bash
set -e

# Stop the running container (if any)
<<<<<<< HEAD
echo "Hi"
=======
containerid= `'docker ps | awk -F " " '{print $1}'`
docker rm -f $containerid
>>>>>>> origin
