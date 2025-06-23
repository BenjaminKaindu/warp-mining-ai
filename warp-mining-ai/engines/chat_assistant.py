"""
Mining Chat Assistant - Natural Language Processing Engine for Mining Questions
"""

import random
import logging
from typing import Dict, List, Any
from config import WarpConfig

logger = logging.getLogger(__name__)

class MiningChatAssistant:
    """Natural language chat assistant specialized in copper and cobalt mining"""
    
    def __init__(self):
        self.config = WarpConfig()
        self.knowledge_base = self._initialize_knowledge_base()
        
        logger.info("Mining Chat Assistant initialized")
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize comprehensive mining knowledge base"""
        
        return {
            'copper_extraction': {
                'oxide_ores': {
                    'methods': ['Sulfuric acid leaching', 'Heap leaching', 'Solvent extraction-electrowinning (SX-EW)'],
                    'process': 'Oxide copper ores are typically processed using hydrometallurgical methods. The ore is crushed and placed on leach pads, where dilute sulfuric acid solution percolates through to dissolve copper minerals.',
                    'chemistry': self.config.COPPER_CHEMISTRY['oxide_leaching'],
                    'optimal_conditions': {
                        'acid_concentration': '10-20 g/L H2SO4',
                        'temperature': '45-65°C',
                        'pH': '1.5-2.5',
                        'contact_time': '6-24 hours'
                    }
                },
                'sulfide_ores': {
                    'methods': ['Froth flotation', 'Smelting', 'Bioleaching'],
                    'process': 'Sulfide copper ores require concentration through flotation followed by pyrometallurgical or hydrometallurgical processing.',
                    'chemistry': self.config.COPPER_CHEMISTRY['sulfide_oxidation'],
                    'challenges': ['Complex mineralogy', 'Lower recovery rates', 'Environmental considerations']
                }
            },
            
            'cobalt_refining': {
                'sources': ['Copper-cobalt ores', 'Nickel laterites', 'Battery recycling'],
                'hydrometallurgical_route': {
                    'steps': ['Roasting', 'Leaching', 'Purification', 'Precipitation', 'Electrowinning'],
                    'chemistry': [
                        self.config.COBALT_CHEMISTRY['sulfide_roasting'],
                        self.config.COBALT_CHEMISTRY['acid_leaching'],
                        self.config.COBALT_CHEMISTRY['precipitation'],
                        self.config.COBALT_CHEMISTRY['electrowinning']
                    ],
                    'advantages': ['High purity product', 'Environmental control', 'Selective separation']
                }
            },
            
            'electrowinning': {
                'copper': {
                    'voltage': '1.8-2.4 V',
                    'current_density': '200-400 A/m²',
                    'temperature': '45-65°C',
                    'electrolyte': 'CuSO4 + H2SO4',
                    'cathode_efficiency': '95-99%',
                    'energy_consumption': '1.8-2.2 kWh/kg Cu'
                },
                'cobalt': {
                    'voltage': '3.0-3.8 V',
                    'current_density': '300-500 A/m²',
                    'temperature': '50-70°C',
                    'electrolyte': 'CoSO4 + H2SO4',
                    'cathode_efficiency': '90-95%',
                    'energy_consumption': '4.5-5.5 kWh/kg Co'
                }
            },
            
            'geological_indicators': {
                'copper_deposits': {
                    'porphyry': ['Alteration halos', 'Quartz-sericite-pyrite zones', 'Potassic alteration'],
                    'sediment_hosted': ['Red bed sequences', 'Structural controls', 'Reducing environments'],
                    'volcanogenic': ['Massive sulfides', 'Hydrothermal vents', 'Bimodal volcanism']
                },
                'cobalt_deposits': {
                    'sedimentary': ['Copper belt sequences', 'Carbonate hosts', 'Organic matter'],
                    'lateritic': ['Weathering profiles', 'Ni-Co associations', 'Clay minerals'],
                    'hydrothermal': ['Quartz veins', 'Arsenide minerals', 'Silver associations']
                }
            },
            
            'process_optimization': {
                'leaching_efficiency': [
                    'Increase temperature (within limits)',
                    'Optimize acid concentration',
                    'Improve ore preparation',
                    'Control particle size distribution'
                ],
                'electrowinning_improvement': [
                    'Optimize current density',
                    'Control electrolyte composition',
                    'Maintain temperature',
                    'Ensure proper anode-cathode spacing'
                ],
                'cost_reduction': [
                    'Energy efficiency improvements',
                    'Reagent consumption optimization',
                    'Process integration',
                    'Waste heat recovery'
                ]
            }
        }
    
    def respond(self, user_input: str) -> str:
        """Generate response to user mining questions"""
        
        user_input_lower = user_input.lower()
        
        # Copper extraction questions
        if any(phrase in user_input_lower for phrase in ['copper extraction', 'extract copper', 'copper leaching']):
            if 'oxide' in user_input_lower:
                return self._explain_copper_oxide_extraction()
            elif 'sulfide' in user_input_lower:
                return self._explain_copper_sulfide_processing()
            else:
                return self._general_copper_extraction()
        
        # Acid concentration questions
        elif any(phrase in user_input_lower for phrase in ['acid concentration', 'sulfuric acid', 'optimal acid']):
            return self._explain_acid_concentration()
        
        # Electrowinning questions
        elif any(phrase in user_input_lower for phrase in ['electrowinning', 'electrowin', 'electrolysis']):
            if 'copper' in user_input_lower:
                return self._explain_copper_electrowinning()
            elif 'cobalt' in user_input_lower:
                return self._explain_cobalt_electrowinning()
            else:
                return self._general_electrowinning()
        
        # Cobalt refining questions
        elif any(phrase in user_input_lower for phrase in ['cobalt refining', 'cobalt processing', 'refine cobalt']):
            return self._explain_cobalt_refining()
        
        # Geological indicators
        elif any(phrase in user_input_lower for phrase in ['geological indicators', 'deposit discovery', 'exploration']):
            if 'copper' in user_input_lower:
                return self._explain_copper_geology()
            elif 'cobalt' in user_input_lower:
                return self._explain_cobalt_geology()
            else:
                return self._general_geology()
        
        # Chemical equations
        elif any(phrase in user_input_lower for phrase in ['chemical equation', 'chemistry', 'reaction']):
            return self._provide_chemical_equations()
        
        # Process optimization
        elif any(phrase in user_input_lower for phrase in ['optimize', 'improve', 'efficiency', 'better']):
            return self._suggest_optimization()
        
        # General mining questions
        elif any(phrase in user_input_lower for phrase in ['mining', 'metallurgy', 'processing']):
            return self._general_mining_info()
        
        # Default response
        else:
            return self._default_response()
    
    def _explain_copper_oxide_extraction(self) -> str:
        """Explain copper oxide ore extraction"""
        info = self.knowledge_base['copper_extraction']['oxide_ores']
        
        response = "🔋 **Copper Oxide Ore Extraction**\\n\\n"
        response += f"**Primary Methods:** {', '.join(info['methods'])}\\n\\n"
        response += f"**Process Overview:**\\n{info['process']}\\n\\n"
        response += f"**Key Chemical Reaction:**\\n`{info['chemistry']}`\\n\\n"
        response += "**Optimal Operating Conditions:**\\n"
        for param, value in info['optimal_conditions'].items():
            response += f"• {param.replace('_', ' ').title()}: {value}\\n"
        
        response += "\\n**💡 Tips:**\\n"
        response += "• Higher temperatures increase leaching kinetics but also costs\\n"
        response += "• Optimal acid concentration balances recovery and reagent consumption\\n"
        response += "• SX-EW produces high-purity copper cathodes directly\\n"
        
        return response
    
    def _explain_copper_sulfide_processing(self) -> str:
        """Explain copper sulfide ore processing"""
        info = self.knowledge_base['copper_extraction']['sulfide_ores']
        
        response = "⚡ **Copper Sulfide Ore Processing**\\n\\n"
        response += f"**Primary Methods:** {', '.join(info['methods'])}\\n\\n"
        response += f"**Process Overview:**\\n{info['process']}\\n\\n"
        response += f"**Key Chemical Reaction:**\\n`{info['chemistry']}`\\n\\n"
        response += "**Main Challenges:**\\n"
        for challenge in info['challenges']:
            response += f"• {challenge}\\n"
        
        response += "\\n**Process Flow:**\\n"
        response += "1. **Grinding** → Reduce particle size for liberation\\n"
        response += "2. **Flotation** → Concentrate copper minerals\\n"
        response += "3. **Smelting** → Produce copper matte\\n"
        response += "4. **Converting** → Remove iron and sulfur\\n"
        response += "5. **Electrorefining** → Achieve 99.99% purity\\n"
        
        return response
    
    def _explain_acid_concentration(self) -> str:
        """Explain optimal acid concentration for leaching"""
        
        response = "🧪 **Optimal Acid Concentration for Leaching**\\n\\n"
        response += "**Copper Oxide Leaching:**\\n"
        response += "• Typical range: 10-20 g/L H₂SO₄\\n"
        response += "• Low acid: Incomplete dissolution\\n"
        response += "• High acid: Excessive reagent costs\\n"
        response += "• Sweet spot: 15 g/L for most operations\\n\\n"
        
        response += "**Factors Affecting Optimal Concentration:**\\n"
        response += "• Ore mineralogy and liberation\\n"
        response += "• Temperature and contact time\\n"
        response += "• Presence of acid-consuming gangue\\n"
        response += "• Economic considerations\\n\\n"
        
        response += "**💡 Optimization Strategy:**\\n"
        response += "• Start with bottle roll tests at lab scale\\n"
        response += "• Test 5, 10, 15, 20, 25 g/L concentrations\\n"
        response += "• Plot recovery vs acid consumption\\n"
        response += "• Consider kinetics and economics\\n"
        
        return response
    
    def _explain_copper_electrowinning(self) -> str:
        """Explain copper electrowinning conditions"""
        ew_info = self.knowledge_base['electrowinning']['copper']
        
        response = "⚡ **Copper Electrowinning Conditions**\\n\\n"
        response += "**Optimal Operating Parameters:**\\n"
        response += f"• Voltage: {ew_info['voltage']}\\n"
        response += f"• Current Density: {ew_info['current_density']}\\n"
        response += f"• Temperature: {ew_info['temperature']}\\n"
        response += f"• Electrolyte: {ew_info['electrolyte']}\\n"
        response += f"• Cathode Efficiency: {ew_info['cathode_efficiency']}\\n"
        response += f"• Energy Consumption: {ew_info['energy_consumption']}\\n\\n"
        
        response += "**Process Chemistry:**\\n"
        response += f"`{self.config.COPPER_CHEMISTRY['electrowinning']}`\\n\\n"
        
        response += "**Key Success Factors:**\\n"
        response += "• Maintain consistent electrolyte composition\\n"
        response += "• Control temperature within ±2°C\\n"
        response += "• Ensure proper current distribution\\n"
        response += "• Regular cathode stripping cycles\\n"
        response += "• Monitor impurity levels (Fe, As, Sb)\\n"
        
        return response
    
    def _explain_cobalt_refining(self) -> str:
        """Explain cobalt refining from sulfide ores"""
        cobalt_info = self.knowledge_base['cobalt_refining']['hydrometallurgical_route']
        
        response = "💎 **Cobalt Refining from Sulfide Ores**\\n\\n"
        response += "**Hydrometallurgical Process Steps:**\\n"
        for i, step in enumerate(cobalt_info['steps'], 1):
            response += f"{i}. **{step}**\\n"
        
        response += "\\n**Key Chemical Reactions:**\\n"
        for i, reaction in enumerate(cobalt_info['chemistry'], 1):
            response += f"{i}. `{reaction}`\\n"
        
        response += "\\n**Process Advantages:**\\n"
        for advantage in cobalt_info['advantages']:
            response += f"• {advantage}\\n"
        
        response += "\\n**💡 Critical Control Points:**\\n"
        response += "• Roasting temperature: 650-700°C\\n"
        response += "• Leaching pH: 1.5-2.5\\n"
        response += "• Selective precipitation sequence\\n"
        response += "• Electrowinning current density: 300-500 A/m²\\n"
        
        return response
    
    def _explain_copper_geology(self) -> str:
        """Explain geological indicators for copper deposits"""
        copper_geo = self.knowledge_base['geological_indicators']['copper_deposits']
        
        response = "🗺️ **Geological Indicators for Copper Deposits**\\n\\n"
        
        response += "**Porphyry Copper Deposits:**\\n"
        for indicator in copper_geo['porphyry']:
            response += f"• {indicator}\\n"
        
        response += "\\n**Sediment-Hosted Deposits:**\\n"
        for indicator in copper_geo['sediment_hosted']:
            response += f"• {indicator}\\n"
        
        response += "\\n**Volcanogenic Massive Sulfides:**\\n"
        for indicator in copper_geo['volcanogenic']:
            response += f"• {indicator}\\n"
        
        response += "\\n**🔍 Exploration Strategy:**\\n"
        response += "• Regional geochemical surveys\\n"
        response += "• Structural mapping and analysis\\n"
        response += "• Geophysical surveys (magnetics, IP)\\n"
        response += "• Target generation and ranking\\n"
        
        return response
    
    def _provide_chemical_equations(self) -> str:
        """Provide key chemical equations for mining processes"""
        
        response = "⚗️ **Key Chemical Equations in Mining**\\n\\n"
        
        response += "**Copper Chemistry:**\\n"
        for process, equation in self.config.COPPER_CHEMISTRY.items():
            response += f"• {process.replace('_', ' ').title()}: `{equation}`\\n"
        
        response += "\\n**Cobalt Chemistry:**\\n"
        for process, equation in self.config.COBALT_CHEMISTRY.items():
            response += f"• {process.replace('_', ' ').title()}: `{equation}`\\n"
        
        response += "\\n**💡 Understanding the Chemistry:**\\n"
        response += "• These equations drive process design\\n"
        response += "• Stoichiometry determines reagent requirements\\n"
        response += "• Thermodynamics predict favorable conditions\\n"
        response += "• Kinetics influence processing time\\n"
        
        return response
    
    def _suggest_optimization(self) -> str:
        """Suggest process optimization strategies"""
        opt_info = self.knowledge_base['process_optimization']
        
        response = "🚀 **Process Optimization Strategies**\\n\\n"
        
        response += "**Improve Leaching Efficiency:**\\n"
        for strategy in opt_info['leaching_efficiency']:
            response += f"• {strategy}\\n"
        
        response += "\\n**Enhance Electrowinning:**\\n"
        for strategy in opt_info['electrowinning_improvement']:
            response += f"• {strategy}\\n"
        
        response += "\\n**Reduce Operating Costs:**\\n"
        for strategy in opt_info['cost_reduction']:
            response += f"• {strategy}\\n"
        
        response += "\\n**💡 Implementation Tips:**\\n"
        response += "• Start with detailed baseline assessment\\n"
        response += "• Implement changes systematically\\n"
        response += "• Monitor key performance indicators\\n"
        response += "• Use statistical process control\\n"
        
        return response
    
    def _general_copper_extraction(self) -> str:
        """General information about copper extraction"""
        
        response = "🔋 **Copper Extraction Overview**\\n\\n"
        response += "Copper extraction methods depend on ore type:\\n\\n"
        response += "**Oxide Ores (15-20% of production):**\\n"
        response += "• Heap leaching with sulfuric acid\\n"
        response += "• Solvent extraction-electrowinning\\n"
        response += "• Direct electrowinning from solutions\\n\\n"
        
        response += "**Sulfide Ores (80-85% of production):**\\n"
        response += "• Froth flotation concentration\\n"
        response += "• Pyrometallurgical smelting\\n"
        response += "• Electrorefining to 99.99% purity\\n\\n"
        
        response += "**💡 Would you like details on a specific method?**\\n"
        response += "Try asking: 'How to extract copper from oxide ores?'"
        
        return response
    
    def _general_electrowinning(self) -> str:
        """General electrowinning information"""
        
        response = "⚡ **Electrowinning Process Overview**\\n\\n"
        response += "Electrowinning uses electrical energy to deposit pure metal from solutions:\\n\\n"
        response += "**Process Principle:**\\n"
        response += "• Metal ions reduced at cathode\\n"
        response += "• Water oxidized at anode\\n"
        response += "• Pure metal deposited on cathodes\\n\\n"
        
        response += "**Applications in Mining:**\\n"
        response += "• Copper from leach solutions\\n"
        response += "• Cobalt from purified electrolytes\\n"
        response += "• Zinc, nickel, and other metals\\n\\n"
        
        response += "**💡 Want specific conditions?**\\n"
        response += "Ask about 'copper electrowinning' or 'cobalt electrowinning'"
        
        return response
    
    def _default_response(self) -> str:
        """Default response for unrecognized queries"""
        
        responses = [
            "🤖 I'm specialized in copper and cobalt mining! Here are some things you can ask me:\\n\\n• How to extract copper from oxide ores?\\n• What's the optimal acid concentration for leaching?\\n• Explain electrowinning conditions\\n• Geological indicators for deposits\\n• Chemical equations in mining\\n\\n**Try asking a specific mining question!**",
            
            "⛏️ I'm your mining AI assistant! I can help with:\\n\\n• Copper extraction processes\\n• Cobalt refining techniques\\n• Electrowinning optimization\\n• Geological exploration\\n• Process chemistry\\n\\n**What would you like to know about mining?**",
            
            "🔬 Ask me about mining processes! I specialize in:\\n\\n• Hydrometallurgy\\n• Pyrometallurgy\\n• Geological indicators\\n• Process optimization\\n• Chemical reactions\\n\\n**What mining topic interests you?**"
        ]
        
        return random.choice(responses)
    
    def _explain_cobalt_electrowinning(self) -> str:
        """Explain cobalt electrowinning conditions"""
        ew_info = self.knowledge_base['electrowinning']['cobalt']
        
        response = "💎 **Cobalt Electrowinning Conditions**\\n\\n"
        response += "**Optimal Operating Parameters:**\\n"
        response += f"• Voltage: {ew_info['voltage']}\\n"
        response += f"• Current Density: {ew_info['current_density']}\\n"
        response += f"• Temperature: {ew_info['temperature']}\\n"
        response += f"• Electrolyte: {ew_info['electrolyte']}\\n"
        response += f"• Cathode Efficiency: {ew_info['cathode_efficiency']}\\n"
        response += f"• Energy Consumption: {ew_info['energy_consumption']}\\n\\n"
        
        response += "**Special Considerations for Cobalt:**\\n"
        response += "• Higher voltage requirement than copper\\n"
        response += "• More sensitive to impurities\\n"
        response += "• Requires careful pH control\\n"
        response += "• Cobalt powder tendency at high current\\n"
        
        return response
    
    def _explain_cobalt_geology(self) -> str:
        """Explain geological indicators for cobalt deposits"""
        cobalt_geo = self.knowledge_base['geological_indicators']['cobalt_deposits']
        
        response = "🗺️ **Geological Indicators for Cobalt Deposits**\\n\\n"
        
        response += "**Sedimentary Copper-Cobalt Deposits:**\\n"
        for indicator in cobalt_geo['sedimentary']:
            response += f"• {indicator}\\n"
        
        response += "\\n**Lateritic Ni-Co Deposits:**\\n"
        for indicator in cobalt_geo['lateritic']:
            response += f"• {indicator}\\n"
        
        response += "\\n**Hydrothermal Cobalt Deposits:**\\n"
        for indicator in cobalt_geo['hydrothermal']:
            response += f"• {indicator}\\n"
        
        return response
    
    def _general_geology(self) -> str:
        """General geology information"""
        
        response = "🗺️ **Geological Indicators for Metal Deposits**\\n\\n"
        response += "Key indicators help identify mineralization:\\n\\n"
        response += "**Structural Controls:**\\n"
        response += "• Fault systems and fracture zones\\n"
        response += "• Contact zones between rock types\\n"
        response += "• Fold hinges and structural highs\\n\\n"
        
        response += "**Geochemical Signatures:**\\n"
        response += "• Pathfinder element anomalies\\n"
        response += "• Alteration mineral assemblages\\n"
        response += "• Stream sediment anomalies\\n\\n"
        
        response += "**💡 Ask specifically about copper or cobalt geology!**"
        
        return response
    
    def _general_mining_info(self) -> str:
        """General mining information"""
        
        response = "⛏️ **Mining & Metallurgy Overview**\\n\\n"
        response += "Modern mining involves multiple stages:\\n\\n"
        response += "**Exploration:**\\n• Geological mapping\\n• Geochemical sampling\\n• Geophysical surveys\\n• Resource estimation\\n\\n"
        response += "**Extraction:**\\n• Open pit or underground mining\\n• Ore preparation and crushing\\n• Concentration processes\\n\\n"
        response += "**Processing:**\\n• Hydrometallurgy (leaching, SX, EW)\\n• Pyrometallurgy (smelting, refining)\\n• Final product purification\\n\\n"
        response += "**💡 Ask about specific processes for detailed information!**"
        
        return response
