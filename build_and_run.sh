#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build --platform linux/amd64 -t challenge1b:latest .

# Run the container with volume mounts for each collection
for collection in 1 2 3; do
    echo -e "\nProcessing Collection $collection..."
    docker run --rm \
      -v "$(pwd)/Collection $collection/PDFs:/app/input" \
      -v "$(pwd)/Collection $collection:/app/output" \
      --network none \
      challenge1b:latest
done