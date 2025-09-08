#!/bin/bash

# Script to copy the consolidated OpenAPI documentation to the context directory
# Usage: ./src/scripts/get-consolidated-doc.sh

set -e

SOURCE_FILE="../trademe-api-doc/openapi/openapi-consolidated.yaml"
DEST_DIR="./context"
DEST_FILE="$DEST_DIR/openapi-consolidated.yaml"

echo "Trade Me SDK - Get Consolidated Documentation"
echo "============================================="

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file not found: $SOURCE_FILE"
    echo "Please ensure the trademe-api.doc repository is cloned at the same level as this project."
    exit 1
fi

# Create destination directory if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    echo "Creating destination directory: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# Copy the file
echo "Copying $SOURCE_FILE to $DEST_FILE"
cp "$SOURCE_FILE" "$DEST_FILE"

echo "✅ Successfully copied OpenAPI consolidated documentation to context directory"
echo "File location: $DEST_FILE"