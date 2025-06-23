#!/bin/bash

# Warp Mining AI Assistant Startup Script
# Self-contained AI for copper and cobalt mining operations

echo "🤖 Starting Warp Mining AI Assistant..."
echo "   Advanced Copper & Cobalt Mining Intelligence System"
echo "   Self-contained AI running on Docker + Ollama + Open Web UI"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed. Please install it first."
    exit 1
fi

echo "✅ Docker is running"
echo "✅ Docker Compose is available"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p mining_data/{ore_samples,extraction_logs,exploration_data,optimization_results}
mkdir -p simulations/{extraction,exploration,optimization}
mkdir -p knowledge/{copper,cobalt,geology,processes}

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

# Start the system
echo "🚀 Starting Warp Mining AI system..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service status
echo ""
echo "🔍 Checking service status..."

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running (port 11434)"
else
    echo "⚠️  Ollama is starting up (may take 5-10 minutes for first run)"
fi

# Check Open Web UI
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Open Web UI is running (port 3000)"
else
    echo "⚠️  Open Web UI is starting up..."
fi

# Check Warp Mining Engine
if curl -s http://localhost:8888/health > /dev/null 2>&1; then
    echo "✅ Warp Mining Engine is running (port 8888)"
else
    echo "⚠️  Warp Mining Engine is starting up..."
fi

echo ""
echo "🎉 Warp Mining AI Assistant is starting up!"
echo ""
echo "📋 Access Points:"
echo "   🌐 Main Interface:    http://localhost:3000"
echo "   🔬 Mining Engine:     http://localhost:8888"  
echo "   🤖 Ollama API:        http://localhost:11434"
echo ""
echo "💡 Getting Started:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Wait for the system to fully initialize (first run may take 5-10 minutes)"
echo "   3. Start asking mining questions or request simulations!"
echo ""
echo "🗣️  Example Questions:"
echo '   • "How do I extract copper from oxide ores?"'
echo '   • "Simulate copper extraction with 2.5% ore grade"'
echo '   • "Optimize for maximum copper purity"'
echo '   • "Analyze mineral potential in Region A"'
echo ""
echo "📊 Mining Capabilities:"
echo "   🗣️  Mining Chat Assistant - Natural language Q&A about mining processes"
echo "   🔬 Extraction Simulator - ML-powered process modeling and predictions"
echo "   🗺️  Exploration Engine - Geological prospectivity analysis"
echo "   ⚡ Optimization Engine - Process parameter optimization"
echo ""
echo "🔧 System Commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop system:   docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""

# Show logs if requested
if [[ "$1" == "--logs" ]]; then
    echo "📋 Showing system logs (Ctrl+C to exit)..."
    docker-compose logs -f
fi

# Wait for user if interactive
if [[ "$1" == "--wait" ]]; then
    echo "Press Enter to continue or Ctrl+C to exit..."
    read
fi

echo "🚀 Warp Mining AI Assistant is ready for mining intelligence!"
echo "   Visit http://localhost:3000 to get started"
