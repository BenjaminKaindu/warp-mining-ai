"""
Warp Mining AI Configuration
"""

import os
from dataclasses import dataclass

@dataclass
class WarpConfig:
    """Configuration settings for Warp Mining AI Assistant"""
    
    # Server configuration
    HOST: str = '0.0.0.0'
    PORT: int = 8888
    DEBUG: bool = False
    
    # Ollama configuration
    OLLAMA_BASE_URL: str = 'http://ollama:11434'
    OLLAMA_MODEL: str = 'llama3.1:latest'
    
    # Mining simulation parameters
    SIMULATION_PRECISION: int = 4
    MAX_SIMULATION_TIME: int = 300  # seconds
    
    # Optimization settings
    OPTIMIZATION_ITERATIONS: int = 100
    CONVERGENCE_THRESHOLD: float = 1e-6
    
    # Data storage paths
    DATA_DIR: str = '/app/data'
    SIMULATION_DIR: str = '/app/simulations'
    KNOWLEDGE_DIR: str = '/app/knowledge'
    
    # Mining knowledge parameters
    COPPER_EXTRACTION_METHODS = [
        'sulfuric_acid_leaching',
        'heap_leaching',
        'solvent_extraction_electrowinning',
        'pyrometallurgy',
        'bioleaching'
    ]
    
    COBALT_REFINING_METHODS = [
        'hydrometallurgical_processing',
        'precipitation_separation',
        'solvent_extraction',
        'electrorefining',
        'selective_precipitation'
    ]
    
    GEOLOGICAL_INDICATORS = [
        'alteration_zones',
        'geochemical_anomalies',
        'structural_controls',
        'lithological_contacts',
        'hydrothermal_systems'
    ]
    
    # Chemical equations and constants
    COPPER_CHEMISTRY = {
        'oxide_leaching': 'CuO + H2SO4 → CuSO4 + H2O',
        'sulfide_oxidation': '2CuFeS2 + 4H2SO4 + O2 → 2CuSO4 + Fe2(SO4)3 + 2S + 4H2O',
        'electrowinning': 'CuSO4 + H2O → Cu + H2SO4 + ½O2',
        'solvent_extraction': 'CuSO4 + 2RH → R2Cu + H2SO4'
    }
    
    COBALT_CHEMISTRY = {
        'sulfide_roasting': '2CoS + 3O2 → 2CoO + 2SO2',
        'acid_leaching': 'CoO + H2SO4 → CoSO4 + H2O',
        'precipitation': 'CoSO4 + Na2S → CoS + Na2SO4',
        'electrowinning': 'Co²⁺ + 2e⁻ → Co'
    }
    
    # ML Model parameters
    ML_MODELS = {
        'random_forest': {
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': 42
        },
        'neural_network': {
            'hidden_layers': [64, 32, 16],
            'activation': 'relu',
            'epochs': 100,
            'batch_size': 32
        },
        'xgboost': {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 6
        }
    }
    
    def __post_init__(self):
        """Initialize derived configurations"""
        # Override with environment variables if available
        self.HOST = os.getenv('WARP_HOST', self.HOST)
        self.PORT = int(os.getenv('WARP_PORT', self.PORT))
        self.DEBUG = os.getenv('WARP_DEBUG', 'false').lower() == 'true'
        self.OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', self.OLLAMA_BASE_URL)
        self.OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', self.OLLAMA_MODEL)
        
        # Create directories if they don't exist
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.SIMULATION_DIR, exist_ok=True)
        os.makedirs(self.KNOWLEDGE_DIR, exist_ok=True)
