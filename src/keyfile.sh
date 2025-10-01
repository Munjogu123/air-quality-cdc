#!/bin/bash
set -e

KEYFILE_DIR="./mongodb-key"
KEYFILE_PATH="$KEYFILE_DIR/mongo-keyfile"

# Make the directory if it doesn't exist
mkdir -p "$KEYFILE_DIR"

# Generate the random key
openssl rand -base64 756 > "$KEYFILE_PATH"

# Change permissions to the file
chmod 400 "$KEYFILE_PATH"
