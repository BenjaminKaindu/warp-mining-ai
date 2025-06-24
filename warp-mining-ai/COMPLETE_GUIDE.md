# 🤖 Warp Mining AI - Complete Guide & Commands

**Advanced Copper & Cobalt Mining Intelligence System**

---

## 📋 Project Overview

**Repository URL**: https://github.com/BenjaminKaindu/warp-mining-ai

Warp Mining AI is a self-contained AI system specifically designed for copper and cobalt mining operations. It combines Large Language Models (via Ollama) with specialized mining simulation engines to provide comprehensive mining intelligence.

### 🌟 Key Features
- **Mining Chat Assistant** - Natural language Q&A about mining processes
- **Extraction Simulator** - ML-powered process modeling and predictions
- **Exploration Engine** - Geological prospectivity analysis
- **Optimization Engine** - Process parameter optimization
- **Self-Contained** - Runs entirely in Docker containers
- **No Internet Required** - Works offline after initial setup

---

## 🚀 Quick Start Commands

### 1. Prerequisites Check
```bash
# Check if Docker is installed
docker --version

# Check if Docker Compose is installed
docker-compose --version

# Start Docker Desktop (if not running)
open -a Docker
```

### 2. Clone the Repository
```bash
git clone https://github.com/BenjaminKaindu/warp-mining-ai.git
cd warp-mining-ai
```

### 3. Start the System (Easiest Method)
```bash
# Make scripts executable (if needed)
chmod +x run-warp.sh
chmod +x deploy.sh

# Run the system
./run-warp.sh
```

### 4. Alternative: Manual Docker Commands
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs

# Stop services
docker-compose down
```

### 5. Access the System
- **Main Interface**: http://localhost:3000
- **Mining Engine**: http://localhost:8888
- **Ollama API**: http://localhost:11434

---

## 📁 Project Structure

```
warp-mining-ai/
├── main.py                    # Main application entry point
├── config.py                  # Configuration settings
├── docker-compose.yml         # Docker orchestration
├── Dockerfile.mining          # Custom mining engine container
├── requirements.txt           # Python dependencies
├── run-warp.sh               # Quick start script
├── deploy.sh                 # GitHub deployment script
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── COMPLETE_GUIDE.md         # This file
├── engines/                  # Core simulation engines
│   ├── chat_assistant.py     # Natural language processing
│   ├── extraction_simulator.py # Process simulation
│   ├── exploration_simulator.py # Geological analysis
│   └── optimization_engine.py # Parameter optimization
├── knowledge/                # Mining knowledge base
├── mining_data/             # Ore samples and extraction logs
├── simulations/             # Simulation results and history
└── templates/               # Web interface templates
```

---

## 🛠️ All Available Commands

### Docker Management
```bash
# Start all services
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View service status
docker-compose ps

# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs ollama
docker-compose logs warp-mining-engine
docker-compose logs open-webui

# Follow logs in real-time
docker-compose logs -f

# Pull latest images
docker-compose pull

# Rebuild containers
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v --remove-orphans
```

### System Health Checks
```bash
# Check if Docker is running
docker info

# Check container health
docker-compose ps

# Test Ollama API
curl http://localhost:11434/api/tags

# Test Mining Engine
curl http://localhost:8888/health

# Test Open Web UI
curl http://localhost:3000
```

### Development Commands
```bash
# Access mining engine container
docker exec -it warp-mining-engine bash

# Run Python scripts inside container
docker exec -it warp-mining-engine python main.py

# Test individual engines
docker exec -it warp-mining-engine python -c "from engines.chat_assistant import MiningChatAssistant; assistant = MiningChatAssistant(); print(assistant.respond('How to extract copper?'))"

# Install additional packages
docker exec -it warp-mining-engine pip install package_name

# View container resources
docker stats
```

### Git Commands
```bash
# Clone repository
git clone https://github.com/BenjaminKaindu/warp-mining-ai.git

# Check status
git status

# Pull latest changes
git pull origin main

# Make changes and commit
git add .
git commit -m "Your commit message"
git push origin main

# View commit history
git log --oneline
```

### Troubleshooting Commands
```bash
# Check Docker space usage
docker system df

# Clean up Docker
docker system prune -a

# View detailed container logs
docker-compose logs --details

# Check port usage
lsof -i :3000
lsof -i :8888
lsof -i :11434

# Monitor system resources
top
htop  # if installed

# Check available disk space
df -h
```

---

## 💬 Usage Examples

### Chat Commands
Once the system is running at http://localhost:3000, try these questions:

```
Mining Process Questions:
- "How do I extract copper from oxide ores?"
- "What's the optimal acid concentration for leaching?"
- "Explain electrowinning conditions for cobalt"
- "What are the geological indicators for copper deposits?"

Simulation Requests:
- "Simulate copper extraction with 2.5% ore grade"
- "Predict electrowinning efficiency at 2.2V and 65°C"
- "Model cobalt leaching with sulfuric acid"
- "Analyze mineral potential in Region A"

Optimization Commands:
- "Optimize for maximum copper purity"
- "Minimize extraction costs while maintaining quality"
- "Improve processing efficiency"
- "Reduce processing time"
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
export WARP_HOST=0.0.0.0
export WARP_PORT=8888
export WARP_DEBUG=false

# Ollama Configuration
export OLLAMA_BASE_URL=http://ollama:11434
export OLLAMA_MODEL=llama3.1:latest

# Mining Engine Features
export SIMULATION_ENGINE=enabled
export EXPLORATION_ENGINE=enabled
export OPTIMIZATION_ENGINE=enabled
```

### Port Configuration
- **3000**: Open Web UI (main interface)
- **8888**: Warp Mining Engine
- **11434**: Ollama API

### Memory Requirements
- **Minimum**: 8GB RAM
- **Recommended**: 16GB RAM
- **GPU**: Optional (for enhanced performance)

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Docker Not Running
```bash
# Check if Docker is running
docker info

# Start Docker Desktop
open -a Docker

# Wait for Docker to start, then retry
```

#### 2. Port Already in Use
```bash
# Check what's using the port
lsof -i :3000

# Kill the process using the port
kill -9 PID_NUMBER

# Or use different ports in docker-compose.yml
```

#### 3. Ollama Model Not Downloading
```bash
# Check Ollama logs
docker-compose logs ollama

# Manually pull the model
docker exec ollama ollama pull llama3.1:latest

# Restart services
docker-compose restart
```

#### 4. Out of Memory
```bash
# Check memory usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Or use a smaller model in docker-compose.yml
```

#### 5. Services Not Starting
```bash
# Check detailed logs
docker-compose logs --details

# Remove containers and restart
docker-compose down
docker-compose up -d

# Check for permission issues
chmod +x run-warp.sh
```

---

## 📊 System Monitoring

### Health Check Commands
```bash
# Overall system health
curl http://localhost:3000 && echo "Web UI: ✅" || echo "Web UI: ❌"
curl http://localhost:8888/health && echo "Mining Engine: ✅" || echo "Mining Engine: ❌"
curl http://localhost:11434/api/tags && echo "Ollama: ✅" || echo "Ollama: ❌"

# Container resource usage
docker stats --no-stream

# Service status
docker-compose ps
```

### Log Monitoring
```bash
# Follow all logs
docker-compose logs -f

# Monitor specific service
docker-compose logs -f ollama

# Save logs to file
docker-compose logs > system_logs.txt
```

---

## 🔄 Backup and Recovery

### Backup Commands
```bash
# Backup entire project
tar -czf warp-mining-ai-backup.tar.gz /Users/macbook/warp-mining-ai

# Backup simulation data
cp -r simulations/ simulations_backup_$(date +%Y%m%d)

# Export Docker images
docker save -o warp-mining-images.tar $(docker-compose config --services)
```

### Recovery Commands
```bash
# Restore from backup
tar -xzf warp-mining-ai-backup.tar.gz

# Restore Docker images
docker load -i warp-mining-images.tar

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 Advanced Usage

### Custom Model Installation
```bash
# Access Ollama container
docker exec -it ollama bash

# Install custom model
ollama pull mistral:latest
ollama pull codellama:latest

# List available models
ollama list

# Update docker-compose.yml to use new model
```

### Adding Custom Mining Data
```bash
# Add new data files
cp your_mining_data.csv mining_data/

# Restart mining engine to reload data
docker-compose restart warp-mining-engine
```

### Performance Optimization
```bash
# Enable GPU support (if available)
# Edit docker-compose.yml to add GPU configuration

# Optimize for memory usage
# Reduce model size or increase Docker memory allocation

# Monitor performance
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 📞 Support and Resources

### Quick Reference
- **Repository**: https://github.com/BenjaminKaindu/warp-mining-ai
- **Main Interface**: http://localhost:3000
- **Mining Engine**: http://localhost:8888
- **Ollama API**: http://localhost:11434

### Essential Commands Summary
```bash
# Start system
./run-warp.sh

# Stop system
docker-compose down

# View logs
docker-compose logs

# Restart system
docker-compose restart

# Health check
docker-compose ps
```

### Emergency Recovery
```bash
# Nuclear option - completely reset
docker-compose down -v --remove-orphans
docker system prune -a
git clean -fdx
./run-warp.sh
```

---

## 🎯 Next Steps

1. **Start the system**: `./run-warp.sh`
2. **Access the interface**: http://localhost:3000
3. **Ask mining questions**: Start with "How do I extract copper?"
4. **Run simulations**: "Simulate copper extraction with 2.5% ore grade"
5. **Optimize processes**: "Optimize for maximum copper purity"

---

**🤖 Warp Mining AI - Self-Contained Intelligence for Mining Excellence**

*Built with ❤️ for the mining industry*

---

*Save this file for quick reference to all commands and procedures!*
