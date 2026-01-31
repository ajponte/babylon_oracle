#!/bin/bash

# Exit on error
set -e

# Navigate to the client directory
cd client

# Install dependencies
echo "Installing client dependencies..."
npm install

# Build the React application
echo "Building client application..."
npm run build

# Run tests
echo "Running client tests..."
npm test
