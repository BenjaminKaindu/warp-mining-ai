"""
Exploration Simulator - Geological Prospectivity Analysis Engine
Simulates mineral exploration using ML classification models
"""

import numpy as np
import pandas as pd
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from config import WarpConfig

logger = logging.getLogger(__name__)

class ExplorationSimulator:
    """Advanced exploration simulation engine for mineral prospectivity"""
    
    def __init__(self):
        self.config = WarpConfig()
        self.models = self._initialize_models()
        self.exploration_history = []
        
        logger.info("Exploration Simulator initialized")
    
    def _initialize_models(self) -> Dict[str, Any]:
        """Initialize simulated ML models for exploration prediction"""
        
        return {
            'random_forest_classifier': {
                'name': 'RandomForestClassifier',
                'features': ['depth', 'soil_ph', 'fe_ppm', 'mg_ppm', 'anomaly_index'],
                'accuracy': 0.91,
                'precision': 0.89,
                'recall': 0.87
            },
            'gradient_boosting': {
                'name': 'GradientBoostingClassifier',
                'features': ['depth', 'soil_ph', 'fe_ppm', 'mg_ppm', 'cu_ppm', 'anomaly_index', 'geological_unit'],
                'accuracy': 0.94,
                'precision': 0.92,
                'recall': 0.90
            },
            'neural_classifier': {
                'name': 'TensorFlow Neural Classifier',
                'architecture': '[128, 64, 32] → ReLU → Softmax',
                'features': ['depth', 'soil_ph', 'fe_ppm', 'mg_ppm', 'cu_ppm', 'co_ppm', 'anomaly_index', 'structural_density'],
                'accuracy': 0.96,
                'precision': 0.94,
                'recall': 0.93
            }
        }
    
    def simulate(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Run exploration simulation with given parameters"""
        
        # Choose model based on parameters
        model_type = self._select_exploration_model(parameters)
        
        # Generate synthetic geological data
        synthetic_data = self._generate_geological_data(parameters)
        
        # Simulate prospectivity analysis
        prospectivity_results = self._analyze_prospectivity(model_type, parameters, synthetic_data)
        
        # Generate exploration recommendations
        recommendations = self._generate_exploration_recommendations(parameters, prospectivity_results)
        
        # Create simulation result
        simulation_result = {
            'timestamp': datetime.now().isoformat(),
            'model_type': model_type,
            'parameters': parameters,
            'prospectivity': prospectivity_results['prospectivity_map'],
            'analysis': prospectivity_results['analysis'],
            'recommendations': recommendations,
            'synthetic_samples': len(synthetic_data),
            'model_accuracy': self.models[model_type]['accuracy']
        }
        
        self.exploration_history.append(simulation_result)
        
        logger.info(f"Exploration simulation completed using {model_type}")
        
        return simulation_result
    
    def _select_exploration_model(self, parameters: Dict[str, Any]) -> str:
        """Select appropriate ML model for exploration"""
        
        sample_count = parameters.get('sample_count', 50)
        
        if sample_count < 30:
            return 'random_forest_classifier'
        elif sample_count < 100:
            return 'gradient_boosting'
        else:
            return 'neural_classifier'
    
    def _generate_geological_data(self, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Generate synthetic geological and geochemical data"""
        
        np.random.seed(42)
        
        sample_count = parameters.get('sample_count', 50)
        survey_area = parameters.get('survey_area', 'Region_A')
        depth_range = parameters.get('depth_range', (0, 200))
        target_mineral = parameters.get('target_mineral', 'copper')
        
        # Generate sample locations
        x_coords = np.random.uniform(0, 1000, sample_count)  # meters
        y_coords = np.random.uniform(0, 1000, sample_count)  # meters
        
        # Generate depth data
        depths = np.random.uniform(depth_range[0], depth_range[1], sample_count)
        
        # Generate geochemical data based on target mineral
        if target_mineral == 'copper':
            data = self._generate_copper_geochemistry(sample_count, x_coords, y_coords, depths)
        elif target_mineral == 'cobalt':
            data = self._generate_cobalt_geochemistry(sample_count, x_coords, y_coords, depths)
        else:
            data = self._generate_general_geochemistry(sample_count, x_coords, y_coords, depths)
        
        # Add location and depth data
        data['x_coordinate'] = x_coords
        data['y_coordinate'] = y_coords
        data['depth'] = depths
        data['survey_area'] = survey_area
        
        return pd.DataFrame(data)
    
    def _generate_copper_geochemistry(self, n_samples: int, x_coords: np.ndarray, 
                                    y_coords: np.ndarray, depths: np.ndarray) -> Dict[str, np.ndarray]:
        """Generate synthetic copper-related geochemical data"""
        
        # Create spatial anomaly zones
        anomaly_centers = [(300, 400), (700, 600)]  # Potential mineralization centers
        
        # Calculate distances to anomaly centers
        distances = []
        for x, y in zip(x_coords, y_coords):
            min_dist = min([np.sqrt((x - cx)**2 + (y - cy)**2) for cx, cy in anomaly_centers])
            distances.append(min_dist)
        distances = np.array(distances)
        
        # Generate copper values with spatial correlation
        cu_background = 20  # ppm
        cu_anomaly_factor = np.exp(-distances / 150)  # Exponential decay
        cu_ppm = cu_background + np.random.lognormal(2, 1, n_samples) * cu_anomaly_factor
        
        # Associated pathfinder elements
        fe_ppm = 30000 + cu_ppm * 50 + np.random.normal(0, 5000, n_samples)  # Iron correlation
        mg_ppm = 15000 + np.random.normal(0, 3000, n_samples)  # Magnesium
        mo_ppm = 2 + cu_ppm * 0.1 + np.random.lognormal(0, 0.5, n_samples)  # Molybdenum
        s_ppm = 500 + cu_ppm * 5 + np.random.normal(0, 200, n_samples)  # Sulfur
        
        # Soil pH (affected by mineralization)
        soil_ph = 6.5 - cu_anomaly_factor * 1.5 + np.random.normal(0, 0.3, n_samples)
        soil_ph = np.clip(soil_ph, 4.0, 8.0)
        
        # Anomaly index (composite indicator)
        anomaly_index = (cu_ppm / cu_background + mo_ppm / 2 + (7 - soil_ph)) / 3
        
        # Geological units (simplified)
        geological_units = np.random.choice(['porphyry', 'sedimentary', 'volcanic'], n_samples, p=[0.4, 0.4, 0.2])
        
        return {
            'cu_ppm': cu_ppm,
            'fe_ppm': fe_ppm,
            'mg_ppm': mg_ppm,
            'mo_ppm': mo_ppm,
            's_ppm': s_ppm,
            'soil_ph': soil_ph,
            'anomaly_index': anomaly_index,
            'geological_unit': geological_units
        }
    
    def _generate_cobalt_geochemistry(self, n_samples: int, x_coords: np.ndarray, 
                                    y_coords: np.ndarray, depths: np.ndarray) -> Dict[str, np.ndarray]:
        """Generate synthetic cobalt-related geochemical data"""
        
        # Create different anomaly pattern for cobalt
        anomaly_centers = [(400, 300), (600, 700)]
        
        distances = []
        for x, y in zip(x_coords, y_coords):
            min_dist = min([np.sqrt((x - cx)**2 + (y - cy)**2) for cx, cy in anomaly_centers])
            distances.append(min_dist)
        distances = np.array(distances)
        
        # Generate cobalt values
        co_background = 15  # ppm
        co_anomaly_factor = np.exp(-distances / 120)
        co_ppm = co_background + np.random.lognormal(1.5, 0.8, n_samples) * co_anomaly_factor
        
        # Associated elements for cobalt deposits
        ni_ppm = 40 + co_ppm * 2 + np.random.normal(0, 20, n_samples)  # Nickel association
        cu_ppm = 25 + co_ppm * 1.5 + np.random.normal(0, 15, n_samples)  # Copper association
        fe_ppm = 35000 + co_ppm * 30 + np.random.normal(0, 6000, n_samples)  # Iron
        mg_ppm = 20000 + np.random.normal(0, 4000, n_samples)  # Magnesium
        
        # Soil chemistry
        soil_ph = 6.8 - co_anomaly_factor * 1.2 + np.random.normal(0, 0.4, n_samples)
        soil_ph = np.clip(soil_ph, 4.5, 8.5)
        
        # Anomaly index for cobalt
        anomaly_index = (co_ppm / co_background + ni_ppm / 40 + cu_ppm / 25) / 3
        
        # Geological units favoring cobalt
        geological_units = np.random.choice(['sedimentary', 'laterite', 'hydrothermal'], n_samples, p=[0.5, 0.3, 0.2])
        
        return {
            'co_ppm': co_ppm,
            'ni_ppm': ni_ppm,
            'cu_ppm': cu_ppm,
            'fe_ppm': fe_ppm,
            'mg_ppm': mg_ppm,
            'soil_ph': soil_ph,
            'anomaly_index': anomaly_index,
            'geological_unit': geological_units
        }
    
    def _generate_general_geochemistry(self, n_samples: int, x_coords: np.ndarray, 
                                     y_coords: np.ndarray, depths: np.ndarray) -> Dict[str, np.ndarray]:
        """Generate general geochemical data"""
        
        # Random background geochemistry
        cu_ppm = np.random.lognormal(2.5, 0.8, n_samples)
        co_ppm = np.random.lognormal(2.0, 0.6, n_samples)
        fe_ppm = np.random.normal(30000, 8000, n_samples)
        mg_ppm = np.random.normal(18000, 5000, n_samples)
        soil_ph = np.random.normal(6.5, 0.8, n_samples)
        
        anomaly_index = np.random.uniform(0.5, 2.0, n_samples)
        geological_units = np.random.choice(['granite', 'basalt', 'sandstone', 'limestone'], n_samples)
        
        return {
            'cu_ppm': cu_ppm,
            'co_ppm': co_ppm,
            'fe_ppm': fe_ppm,
            'mg_ppm': mg_ppm,
            'soil_ph': soil_ph,
            'anomaly_index': anomaly_index,
            'geological_unit': geological_units
        }
    
    def _analyze_prospectivity(self, model_type: str, parameters: Dict[str, Any], 
                             synthetic_data: pd.DataFrame) -> Dict[str, Any]:
        """Simulate ML-based prospectivity analysis"""
        
        model_info = self.models[model_type]
        target_mineral = parameters.get('target_mineral', 'copper')
        
        # Define regions for analysis
        regions = ['Region_A', 'Region_B', 'Region_C', 'Region_D']
        
        # Calculate prospectivity for each region
        prospectivity_map = {}
        
        for region in regions:
            # Simulate model prediction for each region
            probability = self._calculate_region_prospectivity(region, target_mineral, synthetic_data, model_info)
            prospectivity_map[region] = probability
        
        # Generate analysis summary
        analysis = self._generate_prospectivity_analysis(prospectivity_map, target_mineral, model_info)
        
        return {
            'prospectivity_map': prospectivity_map,
            'analysis': analysis
        }
    
    def _calculate_region_prospectivity(self, region: str, target_mineral: str, 
                                      data: pd.DataFrame, model_info: Dict[str, Any]) -> float:
        """Calculate prospectivity probability for a region"""
        
        # Use synthetic data statistics to determine prospectivity
        if target_mineral == 'copper':
            cu_mean = data['cu_ppm'].mean()
            anomaly_mean = data['anomaly_index'].mean()
            ph_mean = data['soil_ph'].mean()
            
            # Copper prospectivity factors
            cu_factor = min(1.0, cu_mean / 50)  # Normalize by threshold
            anomaly_factor = min(1.0, anomaly_mean / 2)
            ph_factor = 1.0 - abs(ph_mean - 5.5) / 3  # Optimal pH around 5.5 for Cu deposits
            
            base_probability = 0.3 + 0.6 * (cu_factor * anomaly_factor * ph_factor)
            
        elif target_mineral == 'cobalt':
            co_mean = data.get('co_ppm', pd.Series([15])).mean()
            ni_mean = data.get('ni_ppm', pd.Series([40])).mean()
            anomaly_mean = data['anomaly_index'].mean()
            
            # Cobalt prospectivity factors
            co_factor = min(1.0, co_mean / 30)
            ni_factor = min(1.0, ni_mean / 60)
            anomaly_factor = min(1.0, anomaly_mean / 2)
            
            base_probability = 0.25 + 0.65 * (co_factor * ni_factor * anomaly_factor)
            
        else:
            # General mineral prospectivity
            anomaly_mean = data['anomaly_index'].mean()
            base_probability = 0.2 + 0.5 * min(1.0, anomaly_mean / 2)
        
        # Add regional variation
        region_factors = {
            'Region_A': 1.2,   # High prospectivity
            'Region_B': 0.8,   # Moderate prospectivity
            'Region_C': 1.0,   # Average prospectivity
            'Region_D': 0.6    # Lower prospectivity
        }
        
        regional_probability = base_probability * region_factors.get(region, 1.0)
        
        # Add model accuracy effect
        accuracy = model_info['accuracy']
        noise = np.random.normal(0, (1 - accuracy) * 0.1)
        
        final_probability = max(0.05, min(0.95, regional_probability + noise))
        
        return final_probability * 100  # Convert to percentage
    
    def _generate_prospectivity_analysis(self, prospectivity_map: Dict[str, float], 
                                       target_mineral: str, model_info: Dict[str, Any]) -> str:
        """Generate detailed prospectivity analysis"""
        
        # Find highest prospectivity region
        best_region = max(prospectivity_map.items(), key=lambda x: x[1])
        worst_region = min(prospectivity_map.items(), key=lambda x: x[1])
        
        analysis = f"Prospectivity analysis for {target_mineral} using {model_info['name']} "
        analysis += f"(Accuracy: {model_info['accuracy']:.1%}).\\n\\n"
        
        analysis += f"**Highest Prospectivity:** {best_region[0]} ({best_region[1]:.1f}% likelihood)\\n"
        analysis += f"**Lowest Prospectivity:** {worst_region[0]} ({worst_region[1]:.1f}% likelihood)\\n\\n"
        
        # Categorize regions
        high_prospects = [region for region, prob in prospectivity_map.items() if prob > 70]
        moderate_prospects = [region for region, prob in prospectivity_map.items() if 40 <= prob <= 70]
        low_prospects = [region for region, prob in prospectivity_map.items() if prob < 40]
        
        if high_prospects:
            analysis += f"**High Priority Targets:** {', '.join(high_prospects)}\\n"
        if moderate_prospects:
            analysis += f"**Moderate Priority Targets:** {', '.join(moderate_prospects)}\\n"
        if low_prospects:
            analysis += f"**Low Priority Areas:** {', '.join(low_prospects)}\\n"
        
        return analysis
    
    def _generate_exploration_recommendations(self, parameters: Dict[str, Any], 
                                            prospectivity_results: Dict[str, Any]) -> List[str]:
        """Generate exploration recommendations based on results"""
        
        recommendations = []
        prospectivity_map = prospectivity_results['prospectivity_map']
        target_mineral = parameters.get('target_mineral', 'copper')
        
        # Find best targets
        high_priority = [region for region, prob in prospectivity_map.items() if prob > 70]
        moderate_priority = [region for region, prob in prospectivity_map.items() if 40 <= prob <= 70]
        
        # Immediate drilling recommendations
        if high_priority:
            recommendations.append(f"Recommend immediate drilling in {', '.join(high_priority)} - high {target_mineral} potential")
        
        # Further exploration recommendations
        if moderate_priority:
            recommendations.append(f"Conduct detailed geochemical surveys in {', '.join(moderate_priority)} before drilling")
        
        # Sample density recommendations
        sample_count = parameters.get('sample_count', 50)
        if sample_count < 100:
            recommendations.append("Increase sample density to 100-150 samples for better statistical confidence")
        
        # Depth recommendations
        depth_range = parameters.get('depth_range', (0, 200))
        if depth_range[1] < 150:
            recommendations.append("Consider deeper sampling (up to 300m) in high-priority areas")
        
        # Multi-element analysis
        if target_mineral == 'copper':
            recommendations.append("Include Mo, Au, and Re analysis for porphyry copper potential assessment")
        elif target_mineral == 'cobalt':
            recommendations.append("Include Ni, Cu, and rare earth element analysis for comprehensive evaluation")
        
        # Geophysical surveys
        max_prob = max(prospectivity_map.values())
        if max_prob > 80:
            recommendations.append("Conduct IP/resistivity surveys to identify sulfide zones in high-priority areas")
        
        # Follow-up recommendations
        if max_prob > 60:
            recommendations.append("Plan systematic grid drilling on 50m x 50m spacing in target areas")
        else:
            recommendations.append("Focus on geological mapping and structural analysis before detailed exploration")
        
        return recommendations
    
    def get_exploration_history(self) -> List[Dict[str, Any]]:
        """Return exploration simulation history"""
        return self.exploration_history
    
    def generate_exploration_targets(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prioritized exploration targets"""
        
        # Run simulation to get prospectivity
        simulation_result = self.simulate(parameters)
        prospectivity_map = simulation_result['prospectivity']
        
        # Rank targets
        sorted_targets = sorted(prospectivity_map.items(), key=lambda x: x[1], reverse=True)
        
        # Generate target details
        targets = []
        for i, (region, probability) in enumerate(sorted_targets):
            priority = "High" if probability > 70 else "Moderate" if probability > 40 else "Low"
            
            target = {
                'rank': i + 1,
                'region': region,
                'probability': f"{probability:.1f}%",
                'priority': priority,
                'recommended_action': self._get_recommended_action(probability),
                'budget_estimate': self._estimate_budget(probability, parameters)
            }
            targets.append(target)
        
        return {
            'targets': targets,
            'total_targets': len(targets),
            'high_priority_count': len([t for t in targets if t['priority'] == 'High']),
            'recommended_budget': sum([t['budget_estimate'] for t in targets[:2]])  # Top 2 targets
        }
    
    def _get_recommended_action(self, probability: float) -> str:
        """Get recommended action based on probability"""
        
        if probability > 80:
            return "Immediate drilling program"
        elif probability > 60:
            return "Detailed geochemical survey + drilling"
        elif probability > 40:
            return "Extended sampling + geophysics"
        else:
            return "Regional reconnaissance only"
    
    def _estimate_budget(self, probability: float, parameters: Dict[str, Any]) -> int:
        """Estimate exploration budget in USD"""
        
        base_budget = 50000  # Base exploration cost
        
        # Adjust based on probability
        if probability > 80:
            budget = base_budget * 3  # Intensive program
        elif probability > 60:
            budget = base_budget * 2  # Moderate program
        elif probability > 40:
            budget = base_budget * 1.5  # Basic program
        else:
            budget = base_budget * 0.5  # Minimal program
        
        # Adjust based on area size and sample count
        sample_count = parameters.get('sample_count', 50)
        budget_multiplier = max(1.0, sample_count / 50)
        
        return int(budget * budget_multiplier)
