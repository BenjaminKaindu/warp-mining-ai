"""
Extraction Simulator - Advanced Mining Process Simulation Engine
Simulates copper and cobalt extraction using ML models
"""

import numpy as np
import pandas as pd
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from config import WarpConfig

logger = logging.getLogger(__name__)

class ExtractionSimulator:
    """Advanced extraction simulation engine using synthetic ML models"""
    
    def __init__(self):
        self.config = WarpConfig()
        self.models = self._initialize_models()
        self.simulation_history = []
        
        logger.info("Extraction Simulator initialized")
    
    def _initialize_models(self) -> Dict[str, Any]:
        """Initialize simulated ML models for extraction prediction"""
        
        return {
            'random_forest': {
                'name': 'RandomForestRegressor',
                'features': ['ore_grade', 'leaching_time', 'acid_concentration', 'temperature', 'voltage'],
                'accuracy': 0.94,
                'mse': 0.0023
            },
            'neural_network': {
                'name': 'TensorFlow Neural Network',
                'architecture': '[64, 32, 16] → ReLU → Output',
                'features': ['ore_grade', 'leaching_time', 'acid_concentration', 'temperature', 'voltage', 'pH'],
                'accuracy': 0.97,
                'mse': 0.0015
            },
            'xgboost': {
                'name': 'XGBoost Regressor',
                'features': ['ore_grade', 'leaching_time', 'acid_concentration', 'temperature', 'voltage', 'particle_size'],
                'accuracy': 0.96,
                'mse': 0.0018
            }
        }
    
    def simulate(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Run extraction simulation with given parameters"""
        
        # Choose model based on complexity
        model_type = self._select_model(parameters)
        
        # Generate synthetic training data
        synthetic_data = self._generate_synthetic_data(parameters)
        
        # Simulate model prediction
        results = self._predict_extraction_performance(model_type, parameters, synthetic_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(parameters, results)
        
        # Store simulation
        simulation_result = {
            'timestamp': datetime.now().isoformat(),
            'model_type': model_type,
            'parameters': parameters,
            'results': results,
            'recommendations': recommendations,
            'synthetic_data_points': len(synthetic_data),
            'model_accuracy': self.models[model_type]['accuracy']
        }
        
        self.simulation_history.append(simulation_result)
        
        logger.info(f"Extraction simulation completed using {model_type}")
        
        return simulation_result
    
    def _select_model(self, parameters: Dict[str, Any]) -> str:
        """Select appropriate ML model based on parameters"""
        
        # Choose model based on number of parameters and complexity
        param_count = len(parameters)
        
        if param_count <= 4:
            return 'random_forest'
        elif param_count <= 6:
            return 'neural_network'
        else:
            return 'xgboost'
    
    def _generate_synthetic_data(self, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Generate synthetic training data for simulation"""
        
        np.random.seed(42)  # For reproducible results
        n_samples = 1000
        
        # Define parameter ranges based on mining industry standards
        param_ranges = {
            'ore_grade': (0.5, 5.0),  # % copper
            'leaching_time': (4, 24),  # hours
            'acid_concentration': (0.5, 3.0),  # mol/L
            'temperature': (25, 85),  # °C
            'voltage': (1.5, 3.5),  # V
            'pH': (1.0, 3.0),
            'particle_size': (1, 50),  # mm
            'pressure': (1, 5),  # atm
            'flow_rate': (10, 100)  # L/min
        }
        
        # Generate synthetic data
        data = {}
        for param, (min_val, max_val) in param_ranges.items():
            if param in parameters:
                # Create variation around user parameter
                base_value = parameters[param]
                variation = 0.2 * base_value  # 20% variation
                data[param] = np.random.normal(base_value, variation, n_samples)
                data[param] = np.clip(data[param], min_val, max_val)
            else:
                # Random values within range
                data[param] = np.random.uniform(min_val, max_val, n_samples)
        
        return pd.DataFrame(data)
    
    def _predict_extraction_performance(self, model_type: str, parameters: Dict[str, Any], 
                                      synthetic_data: pd.DataFrame) -> Dict[str, Any]:
        """Simulate ML model prediction for extraction performance"""
        
        model_info = self.models[model_type]
        
        # Simulate realistic extraction performance based on parameters
        base_recovery = self._calculate_base_recovery(parameters)
        base_purity = self._calculate_base_purity(parameters)
        base_time = self._calculate_processing_time(parameters)
        base_cost = self._calculate_processing_cost(parameters)
        
        # Add model-specific variations and noise
        accuracy = model_info['accuracy']
        noise_factor = (1 - accuracy) * 0.1
        
        recovery = max(0.1, min(0.99, base_recovery + np.random.normal(0, noise_factor)))
        purity = max(0.80, min(0.999, base_purity + np.random.normal(0, noise_factor)))
        processing_time = max(1.0, base_time + np.random.normal(0, base_time * noise_factor))
        processing_cost = max(100, base_cost + np.random.normal(0, base_cost * noise_factor))
        
        # Calculate derived metrics
        energy_consumption = self._calculate_energy_consumption(parameters, processing_time)
        throughput = self._calculate_throughput(parameters, processing_time)
        
        return {
            'copper_recovery': f"{recovery * 100:.1f}%",
            'copper_purity': f"{purity * 100:.2f}%",
            'processing_time': f"{processing_time:.1f} hours",
            'processing_cost': f"${processing_cost:.0f} per tonne",
            'energy_consumption': f"{energy_consumption:.1f} kWh/tonne",
            'throughput': f"{throughput:.1f} tonnes/day",
            'overall_efficiency': f"{(recovery * purity * 100):.1f}%"
        }
    
    def _calculate_base_recovery(self, parameters: Dict[str, Any]) -> float:
        """Calculate base recovery based on process parameters"""
        
        ore_grade = parameters.get('ore_grade', 2.5)
        leaching_time = parameters.get('leaching_time', 8)
        acid_conc = parameters.get('acid_concentration', 1.5)
        temperature = parameters.get('temperature', 65)
        
        # Simplified recovery model based on industry correlations
        grade_factor = min(1.0, ore_grade / 3.0)  # Higher grade = better recovery
        time_factor = min(1.0, leaching_time / 12.0)  # More time = better recovery (with diminishing returns)
        acid_factor = min(1.0, acid_conc / 2.0)  # Optimal acid concentration
        temp_factor = min(1.0, (temperature - 25) / 60.0)  # Higher temp = better kinetics
        
        base_recovery = 0.5 + 0.4 * (grade_factor * time_factor * acid_factor * temp_factor)
        
        # Mineral type adjustments
        mineral_type = parameters.get('mineral_type', 'copper_oxide')
        if mineral_type == 'copper_oxide':
            base_recovery *= 1.1  # Oxides are easier to leach
        elif mineral_type == 'cobalt_sulfide':
            base_recovery *= 0.85  # Sulfides are more challenging
        
        return base_recovery
    
    def _calculate_base_purity(self, parameters: Dict[str, Any]) -> float:
        """Calculate base purity based on process parameters"""
        
        voltage = parameters.get('voltage', 2.2)
        temperature = parameters.get('temperature', 65)
        acid_conc = parameters.get('acid_concentration', 1.5)
        
        # Electrowinning purity model
        voltage_factor = min(1.0, voltage / 2.5)  # Optimal voltage range
        temp_factor = min(1.0, (temperature - 45) / 20.0)  # Temperature control
        acid_factor = 1.0 - abs(acid_conc - 1.5) / 2.0  # Optimal acid concentration
        
        base_purity = 0.85 + 0.14 * (voltage_factor * temp_factor * acid_factor)
        
        return base_purity
    
    def _calculate_processing_time(self, parameters: Dict[str, Any]) -> float:
        """Calculate processing time based on parameters"""
        
        ore_grade = parameters.get('ore_grade', 2.5)
        leaching_time = parameters.get('leaching_time', 8)
        temperature = parameters.get('temperature', 65)
        
        # Base processing time
        base_time = leaching_time
        
        # Adjustments
        if ore_grade < 1.0:
            base_time *= 1.5  # Low grade takes longer
        if temperature < 50:
            base_time *= 1.3  # Low temperature slows kinetics
        
        return base_time
    
    def _calculate_processing_cost(self, parameters: Dict[str, Any]) -> float:
        """Calculate processing cost per tonne"""
        
        acid_conc = parameters.get('acid_concentration', 1.5)
        temperature = parameters.get('temperature', 65)
        voltage = parameters.get('voltage', 2.2)
        processing_time = parameters.get('leaching_time', 8)
        
        # Base costs (USD per tonne)
        reagent_cost = acid_conc * 50  # Acid cost
        energy_cost = (temperature - 25) * 2 + voltage * 30  # Energy cost
        time_cost = processing_time * 15  # Time-related costs
        
        total_cost = 200 + reagent_cost + energy_cost + time_cost  # Base + variable costs
        
        return total_cost
    
    def _calculate_energy_consumption(self, parameters: Dict[str, Any], processing_time: float) -> float:
        """Calculate energy consumption"""
        
        voltage = parameters.get('voltage', 2.2)
        temperature = parameters.get('temperature', 65)
        
        # Energy for electrowinning and heating
        ew_energy = voltage * 0.8 * processing_time  # kWh/tonne
        heating_energy = max(0, (temperature - 25) * 0.1 * processing_time)  # kWh/tonne
        
        return ew_energy + heating_energy
    
    def _calculate_throughput(self, parameters: Dict[str, Any], processing_time: float) -> float:
        """Calculate process throughput"""
        
        # Simplified throughput calculation
        base_throughput = 24 / processing_time * 100  # tonnes/day
        
        # Efficiency adjustments
        ore_grade = parameters.get('ore_grade', 2.5)
        efficiency_factor = min(2.0, ore_grade / 2.0)
        
        return base_throughput * efficiency_factor
    
    def _generate_recommendations(self, parameters: Dict[str, Any], 
                                results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on simulation results"""
        
        recommendations = []
        
        # Extract numeric values from results
        recovery = float(results['copper_recovery'].replace('%', ''))
        purity = float(results['copper_purity'].replace('%', ''))
        cost = float(results['processing_cost'].replace('$', '').replace(' per tonne', ''))
        
        # Recovery optimization
        if recovery < 85:
            ore_grade = parameters.get('ore_grade', 2.5)
            leaching_time = parameters.get('leaching_time', 8)
            temperature = parameters.get('temperature', 65)
            
            if ore_grade < 2.0:
                recommendations.append("Consider ore beneficiation to increase grade before leaching")
            if leaching_time < 10:
                recommendations.append(f"Increase leaching time to {leaching_time + 2}-{leaching_time + 4} hours for better recovery")
            if temperature < 60:
                recommendations.append(f"Increase temperature to 65-70°C to improve leaching kinetics")
        
        # Purity optimization
        if purity < 95:
            voltage = parameters.get('voltage', 2.2)
            acid_conc = parameters.get('acid_concentration', 1.5)
            
            if voltage < 2.0:
                recommendations.append("Increase electrowinning voltage to 2.2-2.4V for higher purity")
            if acid_conc < 1.2 or acid_conc > 2.0:
                recommendations.append("Optimize acid concentration to 1.5-1.8 mol/L for better electrowinning")
        
        # Cost optimization
        if cost > 400:
            acid_conc = parameters.get('acid_concentration', 1.5)
            temperature = parameters.get('temperature', 65)
            
            if acid_conc > 2.0:
                recommendations.append("Reduce acid concentration to minimize reagent costs")
            if temperature > 75:
                recommendations.append("Lower temperature to reduce energy consumption")
        
        # General recommendations
        if recovery > 90 and purity > 95:
            recommendations.append("Excellent performance! Consider scaling up or optimizing for cost reduction")
        
        if not recommendations:
            recommendations.append("Process parameters are well-optimized for current conditions")
        
        return recommendations
    
    def get_simulation_history(self) -> List[Dict[str, Any]]:
        """Return simulation history"""
        return self.simulation_history
    
    def compare_scenarios(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple extraction scenarios"""
        
        results = []
        for i, scenario in enumerate(scenarios):
            result = self.simulate(scenario)
            result['scenario_id'] = f"Scenario_{i+1}"
            results.append(result)
        
        # Find best scenario for different objectives
        best_recovery = max(results, key=lambda x: float(x['results']['copper_recovery'].replace('%', '')))
        best_purity = max(results, key=lambda x: float(x['results']['copper_purity'].replace('%', '')))
        best_cost = min(results, key=lambda x: float(x['results']['processing_cost'].replace('$', '').replace(' per tonne', '')))
        
        comparison = {
            'scenarios': results,
            'best_for_recovery': best_recovery['scenario_id'],
            'best_for_purity': best_purity['scenario_id'],
            'best_for_cost': best_cost['scenario_id'],
            'summary': f"Analyzed {len(scenarios)} scenarios using different ML models"
        }
        
        return comparison
