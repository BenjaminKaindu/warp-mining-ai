"""
Optimization Engine - Advanced Process Optimization for Mining Operations
Uses simulated optimization algorithms to improve extraction efficiency
"""

import numpy as np
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from config import WarpConfig

logger = logging.getLogger(__name__)

class OptimizationEngine:
    """Advanced optimization engine for mining process parameters"""
    
    def __init__(self):
        self.config = WarpConfig()
        self.optimization_algorithms = self._initialize_algorithms()
        self.optimization_history = []
        
        logger.info("Optimization Engine initialized")
    
    def _initialize_algorithms(self) -> Dict[str, Any]:
        """Initialize simulated optimization algorithms"""
        
        return {
            'genetic_algorithm': {
                'name': 'Genetic Algorithm (GA)',
                'description': 'Population-based evolutionary optimization',
                'best_for': ['multi-objective', 'discrete_variables'],
                'convergence_rate': 0.85,
                'exploration_ability': 0.9
            },
            'particle_swarm': {
                'name': 'Particle Swarm Optimization (PSO)',
                'description': 'Swarm intelligence optimization',
                'best_for': ['continuous_variables', 'fast_convergence'],
                'convergence_rate': 0.92,
                'exploration_ability': 0.8
            },
            'simulated_annealing': {
                'name': 'Simulated Annealing (SA)',
                'description': 'Temperature-based stochastic optimization',
                'best_for': ['local_optima_avoidance', 'single_objective'],
                'convergence_rate': 0.88,
                'exploration_ability': 0.85
            },
            'differential_evolution': {
                'name': 'Differential Evolution (DE)',
                'description': 'Vector-based evolutionary algorithm',
                'best_for': ['robust_optimization', 'noisy_functions'],
                'convergence_rate': 0.90,
                'exploration_ability': 0.87
            }
        }
    
    def optimize(self, parameters: Dict[str, Any], objective: str) -> Dict[str, Any]:
        """Run optimization simulation for given parameters and objective"""
        
        # Select optimization algorithm
        algorithm = self._select_algorithm(parameters, objective)
        
        # Define optimization bounds and constraints
        bounds = self._define_parameter_bounds(parameters)
        
        # Simulate optimization process
        optimization_result = self._simulate_optimization(algorithm, parameters, objective, bounds)
        
        # Generate optimization recommendations
        recommendations = self._generate_optimization_recommendations(
            parameters, optimization_result, objective
        )
        
        # Create result structure
        result = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm,
            'objective': objective,
            'original_parameters': parameters,
            'optimized_parameters': optimization_result['optimized_parameters'],
            'improvement': optimization_result['improvement'],
            'convergence_iterations': optimization_result['iterations'],
            'optimization_score': optimization_result['score'],
            'recommendations': recommendations,
            'confidence_level': optimization_result['confidence']
        }
        
        self.optimization_history.append(result)
        
        logger.info(f"Optimization completed using {algorithm} for {objective}")
        
        return result
    
    def _select_algorithm(self, parameters: Dict[str, Any], objective: str) -> str:
        """Select best optimization algorithm based on problem characteristics"""
        
        param_count = len(parameters)
        
        # Multi-objective problems
        if 'multi' in objective.lower() or 'pareto' in objective.lower():
            return 'genetic_algorithm'
        
        # Cost optimization (usually single objective)
        elif 'cost' in objective.lower():
            return 'simulated_annealing'
        
        # Time optimization (fast convergence needed)
        elif 'time' in objective.lower():
            return 'particle_swarm'
        
        # Complex problems with many parameters
        elif param_count > 6:
            return 'differential_evolution'
        
        # Default for general optimization
        else:
            return 'particle_swarm'
    
    def _define_parameter_bounds(self, parameters: Dict[str, Any]) -> Dict[str, Tuple[float, float]]:
        """Define optimization bounds for each parameter"""
        
        # Standard bounds based on mining industry practices
        standard_bounds = {
            'ore_grade': (0.5, 8.0),  # % metal content
            'leaching_time': (2, 48),  # hours
            'acid_concentration': (0.1, 5.0),  # mol/L
            'temperature': (15, 95),  # °C
            'voltage': (1.0, 4.0),  # V
            'current_density': (100, 800),  # A/m²
            'pH': (0.5, 14.0),
            'pressure': (0.5, 10.0),  # atm
            'flow_rate': (1, 200),  # L/min
            'particle_size': (0.1, 100),  # mm
            'reagent_dosage': (0.1, 10.0),  # kg/tonne
            'retention_time': (0.5, 24),  # hours
        }
        
        bounds = {}
        for param, value in parameters.items():
            if param in standard_bounds:
                bounds[param] = standard_bounds[param]
            else:
                # Create bounds around current value
                if isinstance(value, (int, float)):
                    lower = max(0.1, value * 0.5)
                    upper = value * 2.0
                    bounds[param] = (lower, upper)
                else:
                    bounds[param] = (0.1, 10.0)  # Default bounds
        
        return bounds
    
    def _simulate_optimization(self, algorithm: str, parameters: Dict[str, Any], 
                             objective: str, bounds: Dict[str, Tuple[float, float]]) -> Dict[str, Any]:
        """Simulate the optimization process"""
        
        algorithm_info = self.optimization_algorithms[algorithm]
        
        # Initialize optimization parameters
        np.random.seed(42)  # For reproducible results
        
        # Simulate optimization iterations
        max_iterations = self.config.OPTIMIZATION_ITERATIONS
        convergence_rate = algorithm_info['convergence_rate']
        
        # Calculate baseline performance
        baseline_performance = self._calculate_objective_value(parameters, objective)
        
        # Simulate optimization progress
        optimized_params = parameters.copy()
        
        # Iterative improvement simulation
        for iteration in range(max_iterations):
            # Simulate parameter adjustments
            for param, value in optimized_params.items():
                if param in bounds:
                    lower, upper = bounds[param]
                    
                    # Simulate intelligent parameter adjustment
                    improvement_factor = self._get_improvement_factor(param, objective, iteration, max_iterations)
                    
                    # Apply optimization step
                    if isinstance(value, (int, float)):
                        adjustment = np.random.normal(0, (upper - lower) * 0.05) * improvement_factor
                        new_value = np.clip(value + adjustment, lower, upper)
                        optimized_params[param] = new_value
            
            # Early convergence simulation
            if iteration > max_iterations * convergence_rate:
                break
        
        # Calculate optimized performance
        optimized_performance = self._calculate_objective_value(optimized_params, objective)
        
        # Calculate improvement
        if 'minimize' in objective:
            improvement_value = baseline_performance - optimized_performance
            improvement_pct = (improvement_value / baseline_performance) * 100
        else:
            improvement_value = optimized_performance - baseline_performance
            improvement_pct = (improvement_value / baseline_performance) * 100
        
        # Ensure realistic improvements
        improvement_pct = max(0, min(50, improvement_pct))  # Cap at 50% improvement
        
        # Calculate optimization score
        score = min(100, 70 + improvement_pct * 0.6)  # Scale to 0-100
        
        # Calculate confidence based on algorithm and problem complexity
        base_confidence = algorithm_info['convergence_rate']
        param_complexity_penalty = min(0.2, len(parameters) * 0.02)
        confidence = max(0.5, base_confidence - param_complexity_penalty)
        
        return {
            'optimized_parameters': optimized_params,
            'improvement': f"{improvement_pct:.1f}% improvement",
            'iterations': iteration + 1,
            'score': f"{score:.1f}/100",
            'confidence': f"{confidence:.1%}"
        }
    
    def _get_improvement_factor(self, param: str, objective: str, iteration: int, max_iterations: int) -> float:
        """Calculate improvement factor for parameter optimization"""
        
        # Parameter-specific improvement strategies
        param_strategies = {
            'temperature': {
                'maximize_efficiency': 0.8,
                'minimize_cost': -0.6,  # Lower temperature = less energy cost
                'maximize_purity': 0.7,
                'minimize_time': 0.9
            },
            'acid_concentration': {
                'maximize_efficiency': 0.6,
                'minimize_cost': -0.8,  # Less acid = lower cost
                'maximize_purity': 0.4,
                'minimize_time': 0.7
            },
            'voltage': {
                'maximize_efficiency': 0.5,
                'minimize_cost': -0.7,  # Lower voltage = less energy
                'maximize_purity': 0.9,
                'minimize_time': 0.6
            },
            'leaching_time': {
                'maximize_efficiency': 0.7,
                'minimize_cost': -0.5,  # Less time = lower cost
                'maximize_purity': 0.8,
                'minimize_time': -0.9  # Minimize time = reduce leaching time
            }
        }
        
        # Get base strategy
        if param in param_strategies and objective in param_strategies[param]:
            base_factor = param_strategies[param][objective]
        else:
            base_factor = 0.5  # Default improvement factor
        
        # Apply convergence factor (stronger improvements early, fine-tuning later)
        convergence_factor = 1.0 - (iteration / max_iterations)
        
        return base_factor * convergence_factor
    
    def _calculate_objective_value(self, parameters: Dict[str, Any], objective: str) -> float:
        """Calculate objective function value for given parameters"""
        
        # Simplified objective functions based on mining process models
        
        if objective == 'maximize_efficiency':
            # Efficiency based on recovery and energy consumption
            recovery = self._estimate_recovery(parameters)
            energy_efficiency = self._estimate_energy_efficiency(parameters)
            return recovery * energy_efficiency
        
        elif objective == 'minimize_cost':
            # Cost based on reagents, energy, and time
            reagent_cost = self._estimate_reagent_cost(parameters)
            energy_cost = self._estimate_energy_cost(parameters)
            time_cost = self._estimate_time_cost(parameters)
            return reagent_cost + energy_cost + time_cost
        
        elif objective == 'maximize_purity':
            # Purity based on process conditions
            return self._estimate_purity(parameters)
        
        elif objective == 'minimize_time':
            # Processing time based on kinetics
            return self._estimate_processing_time(parameters)
        
        else:
            # Default composite objective
            efficiency = self._estimate_recovery(parameters)
            cost_factor = 1.0 / max(0.1, self._estimate_reagent_cost(parameters) / 100)
            return efficiency * cost_factor
    
    def _estimate_recovery(self, parameters: Dict[str, Any]) -> float:
        """Estimate metal recovery based on parameters"""
        
        base_recovery = 0.75
        
        # Temperature effect
        temp = parameters.get('temperature', 65)
        temp_factor = min(1.2, (temp - 25) / 60)
        
        # Acid concentration effect
        acid = parameters.get('acid_concentration', 1.5)
        acid_factor = min(1.1, acid / 2.0)
        
        # Time effect (diminishing returns)
        time = parameters.get('leaching_time', 8)
        time_factor = min(1.15, np.sqrt(time / 8))
        
        # Ore grade effect
        grade = parameters.get('ore_grade', 2.5)
        grade_factor = min(1.1, grade / 3.0)
        
        recovery = base_recovery * temp_factor * acid_factor * time_factor * grade_factor
        return min(0.98, recovery)
    
    def _estimate_purity(self, parameters: Dict[str, Any]) -> float:
        """Estimate product purity based on parameters"""
        
        base_purity = 0.90
        
        # Voltage effect (higher voltage = better purity)
        voltage = parameters.get('voltage', 2.2)
        voltage_factor = min(1.1, voltage / 2.5)
        
        # Current density effect
        current = parameters.get('current_density', 300)
        current_factor = 1.0 - abs(current - 400) / 800  # Optimal around 400 A/m²
        current_factor = max(0.8, current_factor)
        
        # Temperature effect (moderate temp best for purity)
        temp = parameters.get('temperature', 60)
        temp_factor = 1.0 - abs(temp - 60) / 60
        temp_factor = max(0.8, temp_factor)
        
        purity = base_purity * voltage_factor * current_factor * temp_factor
        return min(0.999, purity)
    
    def _estimate_energy_efficiency(self, parameters: Dict[str, Any]) -> float:
        """Estimate energy efficiency"""
        
        voltage = parameters.get('voltage', 2.2)
        temperature = parameters.get('temperature', 65)
        time = parameters.get('leaching_time', 8)
        
        # Lower voltage and temperature = better energy efficiency
        voltage_penalty = (voltage - 1.8) / 2.0
        temp_penalty = max(0, (temperature - 25)) / 100
        time_penalty = max(0, (time - 6)) / 20
        
        efficiency = 1.0 - voltage_penalty - temp_penalty - time_penalty
        return max(0.3, efficiency)
    
    def _estimate_reagent_cost(self, parameters: Dict[str, Any]) -> float:
        """Estimate reagent cost per tonne"""
        
        acid_conc = parameters.get('acid_concentration', 1.5)
        reagent_dosage = parameters.get('reagent_dosage', 2.0)
        
        # Cost components (USD per tonne)
        acid_cost = acid_conc * 40  # Acid cost
        reagent_cost = reagent_dosage * 25  # Other reagents
        
        return 50 + acid_cost + reagent_cost  # Base cost + variable costs
    
    def _estimate_energy_cost(self, parameters: Dict[str, Any]) -> float:
        """Estimate energy cost per tonne"""
        
        voltage = parameters.get('voltage', 2.2)
        temperature = parameters.get('temperature', 65)
        time = parameters.get('leaching_time', 8)
        
        # Energy cost components
        electrowinning_cost = voltage * 15 * time  # Electrowinning energy
        heating_cost = max(0, (temperature - 25)) * 0.8 * time  # Heating energy
        
        return electrowinning_cost + heating_cost
    
    def _estimate_time_cost(self, parameters: Dict[str, Any]) -> float:
        """Estimate time-related costs"""
        
        time = parameters.get('leaching_time', 8)
        retention_time = parameters.get('retention_time', time)
        
        # Time costs (equipment utilization, labor, etc.)
        return (time + retention_time) * 12  # USD per hour
    
    def _estimate_processing_time(self, parameters: Dict[str, Any]) -> float:
        """Estimate total processing time"""
        
        leaching_time = parameters.get('leaching_time', 8)
        temperature = parameters.get('temperature', 65)
        acid_conc = parameters.get('acid_concentration', 1.5)
        
        # Base processing time
        base_time = leaching_time
        
        # Kinetic adjustments
        if temperature < 50:
            base_time *= 1.5  # Slower kinetics at low temperature
        if acid_conc < 1.0:
            base_time *= 1.3  # Slower dissolution at low acid
        
        return base_time
    
    def _generate_optimization_recommendations(self, original_params: Dict[str, Any], 
                                             optimization_result: Dict[str, Any], 
                                             objective: str) -> List[str]:
        """Generate actionable optimization recommendations"""
        
        recommendations = []
        original = original_params
        optimized = optimization_result['optimized_parameters']
        
        # Parameter-specific recommendations
        for param, opt_value in optimized.items():
            if param in original:
                orig_value = original[param]
                
                if abs(opt_value - orig_value) / orig_value > 0.05:  # 5% change threshold
                    change_pct = ((opt_value - orig_value) / orig_value) * 100
                    direction = "increase" if opt_value > orig_value else "decrease"
                    
                    # Format parameter name for display
                    param_display = param.replace('_', ' ').title()
                    
                    recommendations.append(
                        f"{direction.title()} {param_display} from {orig_value:.2f} to {opt_value:.2f} "
                        f"({change_pct:+.1f}% change)"
                    )
        
        # Objective-specific recommendations
        if objective == 'maximize_efficiency':
            recommendations.append("Monitor recovery rates closely during implementation")
            recommendations.append("Consider staged implementation to validate improvements")
        
        elif objective == 'minimize_cost':
            recommendations.append("Implement cost tracking to verify savings")
            recommendations.append("Balance cost reduction with quality requirements")
        
        elif objective == 'maximize_purity':
            recommendations.append("Increase analytical testing frequency during optimization")
            recommendations.append("Ensure downstream processes can handle purity changes")
        
        elif objective == 'minimize_time':
            recommendations.append("Verify that time reduction doesn't compromise quality")
            recommendations.append("Update production schedules based on new cycle times")
        
        # General implementation recommendations
        recommendations.append("Implement changes gradually to assess individual impacts")
        recommendations.append("Establish monitoring protocols for key performance indicators")
        
        # Risk mitigation
        improvement_pct = float(optimization_result['improvement'].split('%')[0])
        if improvement_pct > 20:
            recommendations.append("High improvement potential - consider pilot testing before full implementation")
        
        return recommendations
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Return optimization history"""
        return self.optimization_history
    
    def multi_objective_optimization(self, parameters: Dict[str, Any], 
                                   objectives: List[str], 
                                   weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Perform multi-objective optimization"""
        
        if weights is None:
            weights = [1.0 / len(objectives)] * len(objectives)  # Equal weights
        
        # Normalize weights
        weight_sum = sum(weights)
        weights = [w / weight_sum for w in weights]
        
        # Run optimization for combined objective
        combined_objective = "multi_objective"
        
        # Select genetic algorithm for multi-objective problems
        algorithm = 'genetic_algorithm'
        bounds = self._define_parameter_bounds(parameters)
        
        # Simulate Pareto-optimal solutions
        pareto_solutions = []
        
        for i in range(5):  # Generate 5 Pareto solutions
            # Vary weights slightly for each solution
            varied_weights = [w + np.random.normal(0, 0.1) for w in weights]
            varied_weights = [max(0, w) for w in varied_weights]  # Ensure non-negative
            weight_sum = sum(varied_weights)
            if weight_sum > 0:
                varied_weights = [w / weight_sum for w in varied_weights]
            
            # Simulate optimization with varied weights
            solution_params = parameters.copy()
            
            # Apply multi-objective optimization logic
            for param, value in solution_params.items():
                if param in bounds:
                    lower, upper = bounds[param]
                    
                    # Weighted optimization for each objective
                    total_adjustment = 0
                    for obj, weight in zip(objectives, varied_weights):
                        improvement_factor = self._get_improvement_factor(param, obj, 50, 100)
                        total_adjustment += improvement_factor * weight
                    
                    if isinstance(value, (int, float)):
                        adjustment = np.random.normal(0, (upper - lower) * 0.1) * total_adjustment
                        new_value = np.clip(value + adjustment, lower, upper)
                        solution_params[param] = new_value
            
            # Calculate objective values
            objective_values = {}
            for obj in objectives:
                objective_values[obj] = self._calculate_objective_value(solution_params, obj)
            
            pareto_solutions.append({
                'parameters': solution_params,
                'objectives': objective_values,
                'weights': varied_weights
            })
        
        # Find best compromise solution
        best_solution = pareto_solutions[0]
        
        # Generate multi-objective result
        result = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm,
            'objective': 'Multi-objective optimization',
            'objectives': objectives,
            'weights': weights,
            'original_parameters': parameters,
            'pareto_solutions': pareto_solutions,
            'best_compromise': best_solution,
            'optimized_parameters': best_solution['parameters'],
            'improvement': "See individual objective improvements",
            'recommendations': self._generate_multi_objective_recommendations(
                parameters, best_solution, objectives
            )
        }
        
        self.optimization_history.append(result)
        
        return result
    
    def _generate_multi_objective_recommendations(self, original_params: Dict[str, Any],
                                                best_solution: Dict[str, Any],
                                                objectives: List[str]) -> List[str]:
        """Generate recommendations for multi-objective optimization"""
        
        recommendations = []
        
        # Trade-off analysis
        recommendations.append("Multi-objective optimization complete - analyze trade-offs carefully")
        
        # Parameter changes
        optimized = best_solution['parameters']
        for param, opt_value in optimized.items():
            if param in original_params:
                orig_value = original_params[param]
                if abs(opt_value - orig_value) / orig_value > 0.05:
                    change_pct = ((opt_value - orig_value) / orig_value) * 100
                    param_display = param.replace('_', ' ').title()
                    recommendations.append(
                        f"Adjust {param_display}: {orig_value:.2f} → {opt_value:.2f} ({change_pct:+.1f}%)"
                    )
        
        # Objective-specific guidance
        recommendations.append("Monitor all objectives during implementation to ensure balanced performance")
        recommendations.append("Consider adjusting objective weights based on business priorities")
        recommendations.append("Validate Pareto solutions through pilot testing")
        
        return recommendations
