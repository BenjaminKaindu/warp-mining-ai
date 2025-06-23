# 🤖 Warp Mining AI Assistant

**Advanced Copper & Cobalt Mining Intelligence System**

Self-contained AI running entirely in Docker using Open Web UI + Ollama + specialized mining engines.

## 🌟 Overview

Warp is a comprehensive AI assistant specifically designed for copper and cobalt mining operations. It combines the power of Large Language Models (via Ollama) with specialized mining simulation engines to provide:

- **Mining Chat Assistant** - Natural language Q&A about mining processes
- **Extraction Simulator** - ML-powered process modeling and predictions  
- **Exploration Engine** - Geological prospectivity analysis
- **Optimization Engine** - Process parameter optimization

## 🚀 Features

### 🗣️ Mining Chat Assistant
Ask natural language questions about:
- Copper extraction from oxide and sulfide ores
- Optimal acid concentrations for leaching
- Electrowinning conditions and parameters
- Cobalt refining processes
- Geological indicators for deposit discovery
- Chemical equations and process chemistry

### 🔬 Simulated Extraction Engine
- **ML Models**: RandomForest, Neural Networks, XGBoost
- **Simulated Features**: Ore grade, leaching time, acid concentration, temperature, voltage
- **Predictions**: Recovery rates, purity levels, processing costs, energy consumption
- **Recommendations**: Automatic optimization suggestions

### 🗺️ Exploration Simulation Engine
- **Geological Analysis**: Soil chemistry, structural controls, anomaly detection
- **ML Classification**: Prospectivity mapping using synthetic geological data
- **Target Generation**: Prioritized exploration targets with budget estimates
- **Risk Assessment**: Confidence levels and drilling recommendations

### ⚡ Optimization Engine
- **Algorithms**: Genetic Algorithm, Particle Swarm, Simulated Annealing, Differential Evolution
- **Objectives**: Maximize efficiency/purity, minimize cost/time
- **Multi-objective**: Pareto optimization with trade-off analysis
- **Implementation**: Staged recommendations with risk mitigation

## 🏗️ Architecture

```
warp-mining-ai/
├── main.py                    # Main application entry point
├── config.py                  # Configuration settings
├── docker-compose.yml         # Docker orchestration
├── Dockerfile.mining          # Custom mining engine container
├── requirements.txt           # Python dependencies
├── engines/                   # Core simulation engines
│   ├── chat_assistant.py      # Natural language processing
│   ├── extraction_simulator.py # Process simulation
│   ├── exploration_simulator.py # Geological analysis
│   └── optimization_engine.py # Parameter optimization
├── knowledge/                 # Mining knowledge base
├── mining_data/              # Ore samples and extraction logs
├── simulations/              # Simulation results and history
└── templates/                # Web interface templates
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB+ RAM recommended
- GPU support optional (for enhanced performance)

### 1. Clone and Setup
```bash
git clone https://github.com/BenjaminKaindu/warp-mining-ai
cd warp-mining-ai
```

### 2. Start the System
```bash
docker-compose up -d
```

This will start:
- **Ollama** (port 11434) - LLM backend
- **Open Web UI** (port 3000) - Main chat interface  
- **Warp Mining Engine** (port 8888) - Specialized mining simulations

### 3. Access the Interface
- **Main Interface**: http://localhost:3000
- **Mining Engine**: http://localhost:8888
- **Ollama API**: http://localhost:11434

### 4. First Time Setup
1. Wait for Ollama to download the model (first startup may take 5-10 minutes)
2. Access the web interface
3. Start asking mining questions or request simulations!

## 💬 Usage Examples

### Mining Questions
```
"How do I extract copper from oxide ores?"
"What's the optimal acid concentration for leaching?"
"Explain electrowinning conditions for cobalt"
"What are the geological indicators for copper deposits?"
```

### Simulation Requests
```
"Simulate copper extraction with 2.5% ore grade"
"Predict electrowinning efficiency at 2.2V and 65°C"
"Model cobalt leaching with sulfuric acid"
"Analyze mineral potential in Region A"
```

### Optimization Commands
```
"Optimize for maximum copper purity"
"Minimize extraction costs while maintaining quality"
"Improve processing efficiency"
"Reduce processing time"
```

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
WARP_HOST=0.0.0.0
WARP_PORT=8888
WARP_DEBUG=false

# Ollama Configuration  
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.1:latest

# Mining Engine Features
SIMULATION_ENGINE=enabled
EXPLORATION_ENGINE=enabled
OPTIMIZATION_ENGINE=enabled
```

### Customization
- **Models**: Modify `config.py` to adjust ML model parameters
- **Knowledge**: Add mining knowledge to `knowledge/` directory
- **Algorithms**: Customize optimization algorithms in `optimization_engine.py`
- **UI**: Modify templates in `templates/` directory

## 🧠 AI Capabilities

### Self-Contained Intelligence
Warp operates entirely within Docker containers and uses:
- **Conceptual Understanding**: Built-in knowledge of mining processes
- **Synthetic Data Generation**: Creates realistic mining data for simulations
- **ML Model Simulation**: Simulates behavior of RandomForest, Neural Networks, XGBoost
- **Process Optimization**: Uses genetic algorithms and swarm intelligence concepts

### No External Dependencies
- ✅ No external APIs required
- ✅ No internet connection needed (after initial setup)
- ✅ No cloud services or external ML platforms
- ✅ Fully contained knowledge base

## 📊 Simulation Examples

### Extraction Simulation Results
```
🔬 Extraction Simulation Complete

Model Used: TensorFlow Neural Network
Parameters:
  • Ore Grade: 2.5%
  • Leaching Time: 8 hours  
  • Acid Concentration: 1.5 mol/L
  • Temperature: 65°C
  • Voltage: 2.2V

Results:
  • Copper Recovery: 89.3%
  • Copper Purity: 95.67%
  • Processing Time: 8.2 hours
  • Processing Cost: $342 per tonne
  • Energy Consumption: 18.4 kWh/tonne
  • Overall Efficiency: 85.2%

💡 Recommendations:
  • Increase temperature to 70°C for better kinetics
  • Consider reducing acid concentration to 1.3 mol/L for cost savings
```

### Exploration Simulation Results
```
🗺️ Exploration Simulation Complete

Model Used: GradientBoostingClassifier
Analysis: Prospectivity analysis for copper using machine learning
classification with 94% accuracy.

Prospectivity Results:
  • Region_A: 87.3% likelihood
  • Region_B: 62.1% likelihood  
  • Region_C: 45.8% likelihood
  • Region_D: 28.4% likelihood

💡 Recommendations:
  • Recommend immediate drilling in Region_A - high copper potential
  • Conduct detailed geochemical surveys in Region_B before drilling
  • Include Mo, Au, and Re analysis for porphyry copper assessment
```

## 🛠️ Development

### Adding New Features
1. **New Engines**: Add to `engines/` directory
2. **Knowledge Expansion**: Update knowledge base in chat assistant
3. **ML Models**: Add new simulation models to extraction engine
4. **Optimization**: Implement new algorithms in optimization engine

### Testing
```bash
# Run unit tests
docker exec warp-mining-engine python -m pytest

# Test individual engines
docker exec warp-mining-engine python -c "from engines.chat_assistant import MiningChatAssistant; assistant = MiningChatAssistant(); print(assistant.respond('How to extract copper?'))"
```

## 📚 Technical Details

### Machine Learning Simulation
Warp simulates the behavior of real ML models using:
- **Statistical Models**: Based on industry correlations and mining engineering principles
- **Synthetic Data**: Generated using realistic parameter distributions
- **Model Accuracy**: Simulated accuracy scores and confidence intervals
- **Realistic Outputs**: Results calibrated to match actual mining operations

### Process Engineering
Built-in knowledge of:
- **Hydrometallurgy**: Leaching, solvent extraction, electrowinning
- **Pyrometallurgy**: Smelting, converting, refining
- **Geology**: Ore types, geological indicators, exploration methods
- **Optimization**: Process control, parameter tuning, cost optimization

## 🔒 Security & Privacy

- **Offline Operation**: No external data transmission
- **Local Processing**: All computations performed locally
- **Data Privacy**: No mining data leaves your environment
- **Self-Contained**: Complete independence from external services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new mining capabilities or improve existing ones
4. Test thoroughly with Docker environment
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Ollama not starting:**
```bash
docker-compose logs ollama
# Wait for model download to complete
```

**Out of memory:**
```bash
# Reduce model size in docker-compose.yml
# Or increase Docker memory allocation
```

**Simulation errors:**
```bash
# Check mining engine logs
docker-compose logs warp-mining-engine
```

### Documentation
- [Mining Process Guide](docs/mining-processes.md)
- [Simulation Engine API](docs/simulation-api.md)  
- [Optimization Algorithms](docs/optimization.md)
- [Knowledge Base](docs/knowledge-base.md)

---

**🤖 Warp Mining AI - Self-Contained Intelligence for Mining Excellence**

*Built with ❤️ for the mining industry*
