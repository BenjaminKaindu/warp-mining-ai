#!/bin/bash

# Warp Mining AI - Deployment Script
# This script sets up GitHub repository and runs the system

echo "🤖 Warp Mining AI - Deployment Script"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Please run this script from the warp-mining-ai directory."
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI not found. Installing via Homebrew..."
    brew install gh
fi

# GitHub Setup
echo
print_status "Setting up GitHub repository..."
echo

# Check if user is authenticated with GitHub CLI
if ! gh auth status &> /dev/null; then
    print_warning "You need to authenticate with GitHub CLI first."
    echo
    echo "Please run the following commands to authenticate:"
    echo "1. gh auth login"
    echo "2. Follow the web authentication flow"
    echo "3. Select HTTPS as your preferred protocol"
    echo "4. Re-run this script after authentication"
    echo
    read -p "Have you completed GitHub CLI authentication? (y/n): " auth_completed
    
    if [ "$auth_completed" != "y" ] && [ "$auth_completed" != "Y" ]; then
        print_warning "Please complete GitHub authentication and re-run this script."
        exit 1
    fi
fi

# Get GitHub username
GITHUB_USERNAME=$(gh api user --jq '.login' 2>/dev/null)
if [ -z "$GITHUB_USERNAME" ]; then
    print_error "Could not get GitHub username. Please ensure you're properly authenticated."
    exit 1
fi

print_success "Authenticated as: $GITHUB_USERNAME"

# Create GitHub repository
print_status "Creating GitHub repository: $GITHUB_USERNAME/warp-mining-ai"

if gh repo create warp-mining-ai --public --description "Advanced Copper & Cobalt Mining Intelligence System - Self-contained AI running entirely in Docker using Open Web UI + Ollama + specialized mining engines" --clone=false; then
    print_success "GitHub repository created successfully!"
    
    # Add remote origin
    git remote add origin "https://github.com/$GITHUB_USERNAME/warp-mining-ai.git"
    
    # Update README with actual username
    sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
    rm README.md.bak
    
    # Commit the updated README
    git add README.md
    git commit -m "Update README with actual GitHub username"
    
    # Push to GitHub
    print_status "Pushing code to GitHub..."
    git push -u origin main
    
    print_success "Code pushed to GitHub successfully!"
    echo
    print_success "🌐 Repository URL: https://github.com/$GITHUB_USERNAME/warp-mining-ai"
    
else
    print_warning "Repository might already exist or there was an error creating it."
    print_status "Checking if remote origin exists..."
    
    if git remote get-url origin &> /dev/null; then
        print_success "Remote origin already configured."
    else
        print_status "Adding remote origin..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/warp-mining-ai.git"
    fi
    
    # Try to push anyway
    print_status "Attempting to push to existing repository..."
    git push -u origin main
fi

echo
echo "========================================"
print_success "🚀 GitHub Setup Complete!"
echo "========================================"
echo

# System Deployment
print_status "Starting Warp Mining AI system..."
echo

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Stop any existing containers
print_status "Stopping any existing containers..."
docker-compose down

# Pull latest images and start services
print_status "Starting services (this may take a few minutes on first run)..."
docker-compose up -d

# Wait for services to start
print_status "Waiting for services to initialize..."
sleep 10

# Check service status
print_status "Checking service status..."

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running!"
    echo
    echo "🌐 Access your Warp Mining AI system at:"
    echo "   • Main Interface: http://localhost:3000"
    echo "   • Mining Engine:  http://localhost:8888"
    echo "   • Ollama API:     http://localhost:11434"
    echo
    echo "📚 Try asking questions like:"
    echo "   • 'How do I extract copper from oxide ores?'"
    echo "   • 'Simulate copper extraction with 2.5% ore grade'"
    echo "   • 'Optimize for maximum copper purity'"
    echo
    print_warning "Note: First startup may take 5-10 minutes for Ollama to download the model."
    echo
    print_success "🎉 Warp Mining AI is now running and available on GitHub!"
    print_success "Repository: https://github.com/$GITHUB_USERNAME/warp-mining-ai"
    
else
    print_error "Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo
echo "========================================"
print_success "✅ Deployment Complete!"
echo "========================================"
