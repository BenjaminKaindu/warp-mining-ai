#!/usr/bin/env python3
"""
Warp Mining AI Assistant - Main Application
Self-contained AI system for copper and cobalt mining operations
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from engines.chat_assistant import MiningChatAssistant
from engines.extraction_simulator import ExtractionSimulator
from engines.exploration_simulator import ExplorationSimulator
from engines.optimization_engine import OptimizationEngine
from config import WarpConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WarpMiningAI:
    """Main Warp Mining AI Assistant System"""
    
    def __init__(self):
        self.config = WarpConfig()
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'warp-mining-ai-2024'
        
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Initialize engines
        self.chat_assistant = MiningChatAssistant()
        self.extraction_simulator = ExtractionSimulator()
        self.exploration_simulator = ExplorationSimulator()
        self.optimization_engine = OptimizationEngine()
        
        # Conversation history
        self.conversation_history = []
        
        self.setup_routes()
        self.setup_socket_events()
        
        logger.info("Warp Mining AI Assistant initialized successfully")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template_string(self.get_main_template())
        
        @self.app.route('/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'engines': {
                    'chat_assistant': True,
                    'extraction_simulator': True,
                    'exploration_simulator': True,
                    'optimization_engine': True
                }
            })
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.get_json()
            user_input = data.get('message', '')
            
            if not user_input:
                return jsonify({'error': 'No message provided'}), 400
            
            try:
                response = self.process_user_input(user_input)
                self.conversation_history.append({
                    'user': user_input,
                    'assistant': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error processing chat: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/simulate', methods=['POST'])
        def simulate():
            data = request.get_json()
            simulation_type = data.get('type', 'extraction')
            parameters = data.get('parameters', {})
            
            try:
                if simulation_type == 'extraction':
                    result = self.extraction_simulator.simulate(parameters)
                elif simulation_type == 'exploration':
                    result = self.exploration_simulator.simulate(parameters)
                else:
                    return jsonify({'error': 'Invalid simulation type'}), 400
                
                return jsonify(result)
            except Exception as e:
                logger.error(f"Error in simulation: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/optimize', methods=['POST'])
        def optimize():
            data = request.get_json()
            parameters = data.get('parameters', {})
            objective = data.get('objective', 'maximize_purity')
            
            try:
                result = self.optimization_engine.optimize(parameters, objective)
                return jsonify(result)
            except Exception as e:
                logger.error(f"Error in optimization: {str(e)}")
                return jsonify({'error': str(e)}), 500
    
    def setup_socket_events(self):
        """Setup SocketIO events for real-time communication"""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info('Client connected to Warp Mining AI')
            emit('status', {'message': 'Connected to Warp Mining AI Assistant'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info('Client disconnected from Warp Mining AI')
        
        @self.socketio.on('chat_message')
        def handle_chat_message(data):
            user_input = data.get('message', '')
            if user_input:
                response = self.process_user_input(user_input)
                emit('chat_response', {
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
    
    def process_user_input(self, user_input):
        """Process user input and route to appropriate engine"""
        
        user_input_lower = user_input.lower()
        
        # Check for simulation requests
        if any(word in user_input_lower for word in ['simulate', 'simulation', 'predict', 'model']):
            if any(word in user_input_lower for word in ['extract', 'leach', 'electrowin', 'refin']):
                return self.handle_extraction_simulation(user_input)
            elif any(word in user_input_lower for word in ['explor', 'prospect', 'deposit', 'geological']):
                return self.handle_exploration_simulation(user_input)
        
        # Check for optimization requests
        elif any(word in user_input_lower for word in ['optimize', 'improve', 'better', 'efficiency']):
            return self.handle_optimization(user_input)
        
        # Default to chat assistant
        else:
            return self.chat_assistant.respond(user_input)
    
    def handle_extraction_simulation(self, user_input):
        """Handle extraction simulation requests"""
        # Parse parameters from user input (simplified)
        parameters = self.parse_extraction_parameters(user_input)
        
        # Run simulation
        result = self.extraction_simulator.simulate(parameters)
        
        # Format response
        response = f"🔬 **Extraction Simulation Complete**\\n\\n"
        response += f"**Model Used:** {result['model_type']}\\n"
        response += f"**Parameters:**\\n"
        for key, value in result['parameters'].items():
            response += f"  • {key}: {value}\\n"
        response += f"\\n**Results:**\\n"
        for key, value in result['results'].items():
            response += f"  • {key}: {value}\\n"
        
        if result.get('recommendations'):
            response += f"\\n**💡 Recommendations:**\\n"
            for rec in result['recommendations']:
                response += f"  • {rec}\\n"
        
        return response
    
    def handle_exploration_simulation(self, user_input):
        """Handle exploration simulation requests"""
        parameters = self.parse_exploration_parameters(user_input)
        result = self.exploration_simulator.simulate(parameters)
        
        response = f"🗺️ **Exploration Simulation Complete**\\n\\n"
        response += f"**Model Used:** {result['model_type']}\\n"
        response += f"**Analysis:** {result['analysis']}\\n"
        response += f"\\n**Prospectivity Results:**\\n"
        for location, probability in result['prospectivity'].items():
            response += f"  • {location}: {probability:.1f}% likelihood\\n"
        
        if result.get('recommendations'):
            response += f"\\n**💡 Recommendations:**\\n"
            for rec in result['recommendations']:
                response += f"  • {rec}\\n"
        
        return response
    
    def handle_optimization(self, user_input):
        """Handle optimization requests"""
        parameters = self.parse_optimization_parameters(user_input)
        objective = self.extract_objective(user_input)
        
        result = self.optimization_engine.optimize(parameters, objective)
        
        response = f"⚡ **Optimization Complete**\\n\\n"
        response += f"**Objective:** {result['objective']}\\n"
        response += f"**Algorithm:** {result['algorithm']}\\n"
        response += f"\\n**Optimized Parameters:**\\n"
        for param, value in result['optimized_parameters'].items():
            response += f"  • {param}: {value}\\n"
        
        response += f"\\n**Expected Improvement:** {result['improvement']}\\n"
        
        if result.get('recommendations'):
            response += f"\\n**💡 Next Steps:**\\n"
            for rec in result['recommendations']:
                response += f"  • {rec}\\n"
        
        return response
    
    def parse_extraction_parameters(self, user_input):
        """Extract parameters from user input for extraction simulation"""
        # Simplified parameter extraction - in reality, this would be more sophisticated
        defaults = {
            'ore_grade': 2.5,  # %
            'leaching_time': 8,  # hours
            'acid_concentration': 1.5,  # mol/L
            'temperature': 65,  # °C
            'voltage': 2.2,  # V
            'mineral_type': 'copper_oxide'
        }
        
        # Basic keyword extraction
        if 'cobalt' in user_input.lower():
            defaults['mineral_type'] = 'cobalt_sulfide'
        
        # Extract numbers and associate with likely parameters
        import re
        numbers = re.findall(r'\\d+\\.?\\d*', user_input)
        
        return defaults
    
    def parse_exploration_parameters(self, user_input):
        """Extract parameters for exploration simulation"""
        return {
            'survey_area': 'Region_A',
            'sample_count': 50,
            'depth_range': (0, 200),
            'target_mineral': 'copper' if 'copper' in user_input.lower() else 'cobalt'
        }
    
    def parse_optimization_parameters(self, user_input):
        """Extract parameters for optimization"""
        return {
            'current_efficiency': 0.85,
            'cost_constraint': 1000,
            'time_constraint': 12,
            'quality_target': 0.95
        }
    
    def extract_objective(self, user_input):
        """Extract optimization objective from user input"""
        if any(word in user_input.lower() for word in ['cost', 'cheap', 'economic']):
            return 'minimize_cost'
        elif any(word in user_input.lower() for word in ['time', 'fast', 'quick']):
            return 'minimize_time'
        elif any(word in user_input.lower() for word in ['purity', 'quality', 'grade']):
            return 'maximize_purity'
        else:
            return 'maximize_efficiency'
    
    def get_main_template(self):
        """Return the main HTML template"""
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Warp Mining AI Assistant</title>
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    min-height: 100vh;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .header h1 {
                    font-size: 2.5em;
                    margin: 0;
                    background: linear-gradient(45deg, #ffd700, #ff8c00);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                .header p {
                    font-size: 1.2em;
                    opacity: 0.9;
                    margin: 10px 0;
                }
                .chat-container {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    min-height: 400px;
                    margin-bottom: 20px;
                }
                .chat-messages {
                    height: 300px;
                    overflow-y: auto;
                    margin-bottom: 15px;
                    padding: 10px;
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                }
                .message {
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 10px;
                }
                .user-message {
                    background: rgba(255, 215, 0, 0.2);
                    text-align: right;
                }
                .assistant-message {
                    background: rgba(0, 255, 127, 0.2);
                    text-align: left;
                }
                .input-area {
                    display: flex;
                    gap: 10px;
                }
                .input-area input {
                    flex: 1;
                    padding: 12px;
                    border: none;
                    border-radius: 25px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    font-size: 16px;
                }
                .input-area button {
                    padding: 12px 25px;
                    border: none;
                    border-radius: 25px;
                    background: linear-gradient(45deg, #ffd700, #ff8c00);
                    color: white;
                    font-weight: bold;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                .input-area button:hover {
                    transform: scale(1.05);
                }
                .capabilities {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                .capability-card {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                .capability-card h3 {
                    color: #ffd700;
                    margin-top: 0;
                }
                .status {
                    text-align: center;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 10px;
                    background: rgba(0, 255, 127, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 Warp Mining AI Assistant</h1>
                    <p>Advanced Copper & Cobalt Mining Intelligence System</p>
                    <p>Self-contained AI running on Docker + Ollama + Open Web UI</p>
                </div>
                
                <div id="status" class="status">
                    Ready to assist with mining operations...
                </div>
                
                <div class="chat-container">
                    <div id="chatMessages" class="chat-messages"></div>
                    <div class="input-area">
                        <input type="text" id="messageInput" placeholder="Ask me about copper/cobalt mining, request simulations, or optimization..." maxlength="500">
                        <button onclick="sendMessage()">Send</button>
                    </div>
                </div>
                
                <div class="capabilities">
                    <div class="capability-card">
                        <h3>🗣️ Mining Chat Assistant</h3>
                        <p>Ask natural language questions about:</p>
                        <ul>
                            <li>Copper extraction from oxide ores</li>
                            <li>Optimal acid concentrations</li>
                            <li>Electrowinning conditions</li>
                            <li>Cobalt refining processes</li>
                            <li>Geological indicators</li>
                            <li>Chemical equations</li>
                        </ul>
                    </div>
                    
                    <div class="capability-card">
                        <h3>🔬 Extraction Simulator</h3>
                        <p>Request simulations like:</p>
                        <ul>
                            <li>"Simulate copper extraction with 2.5% ore grade"</li>
                            <li>"Predict electrowinning efficiency at 2.2V"</li>
                            <li>"Model cobalt leaching with sulfuric acid"</li>
                        </ul>
                        <p>Uses RandomForest and Neural Network models</p>
                    </div>
                    
                    <div class="capability-card">
                        <h3>🗺️ Exploration Engine</h3>
                        <p>Geological prospectivity analysis:</p>
                        <ul>
                            <li>"Analyze mineral potential in Region A"</li>
                            <li>"Predict copper deposits from soil samples"</li>
                            <li>"Simulate exploration survey results"</li>
                        </ul>
                        <p>ML classification for deposit discovery</p>
                    </div>
                    
                    <div class="capability-card">
                        <h3>⚡ Optimization Engine</h3>
                        <p>Process optimization suggestions:</p>
                        <ul>
                            <li>"Optimize for maximum copper purity"</li>
                            <li>"Reduce extraction costs while maintaining quality"</li>
                            <li>"Minimize processing time"</li>
                        </ul>
                        <p>Automatic parameter tuning and recommendations</p>
                    </div>
                </div>
            </div>
            
            <script>
                const socket = io();
                
                socket.on('connect', function() {
                    document.getElementById('status').textContent = 'Connected to Warp Mining AI Assistant';
                });
                
                socket.on('chat_response', function(data) {
                    addMessage('assistant', data.response);
                });
                
                socket.on('status', function(data) {
                    document.getElementById('status').textContent = data.message;
                });
                
                function sendMessage() {
                    const input = document.getElementById('messageInput');
                    const message = input.value.trim();
                    
                    if (message) {
                        addMessage('user', message);
                        socket.emit('chat_message', {'message': message});
                        input.value = '';
                    }
                }
                
                function addMessage(sender, text) {
                    const chatMessages = document.getElementById('chatMessages');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${sender}-message`;
                    
                    // Convert markdown-style formatting to HTML
                    const formattedText = text
                        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                        .replace(/\\n/g, '<br>');
                    
                    messageDiv.innerHTML = formattedText;
                    chatMessages.appendChild(messageDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
                
                // Enter key support
                document.getElementById('messageInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
                
                // Welcome message
                setTimeout(() => {
                    addMessage('assistant', '🤖 **Welcome to Warp Mining AI!**\\n\\nI am your specialized assistant for copper and cobalt mining operations. I can help you with:\\n\\n• **Mining questions** - Ask me anything about extraction, refining, or geology\\n• **Simulations** - Request process modeling and predictions\\n• **Optimization** - Get recommendations to improve efficiency\\n\\n**Try asking:** "How do I extract copper from oxide ores?" or "Simulate copper extraction with 2% ore grade"');
                }, 1000);
            </script>
        </body>
        </html>
        '''
    
    def run(self):
        """Start the Warp Mining AI Assistant"""
        host = self.config.HOST
        port = self.config.PORT
        debug = self.config.DEBUG
        
        logger.info(f"Starting Warp Mining AI Assistant on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    warp = WarpMiningAI()
    warp.run()
