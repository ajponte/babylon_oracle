#!/bin/bash

# Navigate to the client directory
cd client

# Install dependencies
echo "Installing client dependencies..."
npm install

# Build the React application
echo "Building client application..."
npm run build

# Start the client server
echo "Starting client server..."
npm start
