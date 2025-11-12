#!/bin/bash

set -e

echo "🚀 Setting up local development environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it first."
    exit 1
fi

# Check if src/.env exists
if [ ! -f src/.env ]; then
    echo "❌ src/.env file not found. Please create it first."
    exit 1
fi

# Check if frontend/.env.local exists
if [ ! -f frontend/.env.local ]; then
    echo "❌ frontend/.env.local file not found. Please create it first."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '#' | xargs)

# Generate nginx config
echo "📝 Generating nginx configuration..."
./scripts/generate-nginx-config.sh

# Build and start containers
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

echo "✅ Local environment is ready!"
echo ""
echo "🌐 Access your app at: http://localhost"
echo "🔧 Backend API: http://localhost/api"
echo "📊 View logs: docker-compose logs -f"