"""
Warp Mining AI Engines Package
Specialized engines for mining operations simulation and optimization
"""

from .chat_assistant import MiningChatAssistant
from .extraction_simulator import ExtractionSimulator
from .exploration_simulator import ExplorationSimulator
from .optimization_engine import OptimizationEngine

__all__ = [
    'MiningChatAssistant',
    'ExtractionSimulator', 
    'ExplorationSimulator',
    'OptimizationEngine'
]

__version__ = '1.0.0'
__author__ = 'Warp Mining AI Team'
__description__ = 'Advanced mining intelligence engines for copper and cobalt operations'
