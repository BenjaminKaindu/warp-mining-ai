#!/bin/bash

# Warp Mining AI - Quick Run Script
# Simple command to start the system

echo "🤖 Starting Warp Mining AI..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start the services
print_status "Starting Warp Mining AI services..."
docker-compose up -d

# Wait a moment for services to initialize
sleep 5

# Check status
if docker-compose ps | grep -q "Up"; then
    print_success "Warp Mining AI is running!"
    echo
    echo "🌐 Access your system at:"
    echo "   • Main Interface: http://localhost:3000"
    echo "   • Mining Engine:  http://localhost:8888"
    echo "   • Ollama API:     http://localhost:11434"
    echo
    echo "📚 Try asking questions like:"
    echo "   • 'How do I extract copper from oxide ores?'"
    echo "   • 'Simulate copper extraction with 2.5% ore grade'"
    echo "   • 'Optimize for maximum copper purity'"
    echo
    echo "🛑 To stop: docker-compose down"
    
else
    print_error "Failed to start services. Check logs: docker-compose logs"
fi
