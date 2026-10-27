"""
P-Brain: Enhanced Neural Network Architecture
Brain-inspired multi-region neural network with optimized sparse connections
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import time


class BrainRegion:
    """Specialized brain region with specific function"""
    
    REGIONS = {
        "sensory": {"neurons": 32, "description": "Input processing"},
        "sensory_hidden": {"neurons": 48, "description": "Feature extraction"},
        "memory": {"neurons": 64, "description": "Memory association"},
        "emotion": {"neurons": 32, "description": "Emotional processing"},
        "language": {"neurons": 48, "description": "Broca's area - language"},
        "integration": {"neurons": 64, "description": "Cross-modal integration"},
        "reward": {"neurons": 16, "description": "Dopamine/reward processing"},
        "decision": {"neurons": 32, "description": "Decision making"},
        "motor": {"neurons": 16, "description": "Output/expression control"},
    }
    
    def __init__(self, name: str, neuron_count: int, input_size: int):
        self.name = name
        self.neuron_count = neuron_count
        self.input_size = input_size
        
        # Sparse connectivity (like real brain - not fully connected)
        # Each neuron connects to ~60% of inputs
        self.connection_density = 0.6
        self.connections = self._create_sparse_connections()
        
        # Weights and biases (larger initial weights for better activation)
        self.weights = np.random.randn(neuron_count, input_size) * 0.5 * self.connections
        self.biases = np.random.randn(neuron_count) * 0.1
        
        # Activity tracking
        self.activity = np.zeros(neuron_count)
        self.total_activations = 0
    
    def _create_sparse_connections(self) -> np.ndarray:
        """Create sparse connection matrix (like real brain)"""
        mask = np.random.random((self.neuron_count, self.input_size)) < self.connection_density
        return mask.astype(float)
    
    def activate(self, inputs: np.ndarray) -> np.ndarray:
        """Forward pass through region"""
        # Weighted sum with sparse connections
        weighted = np.dot(self.weights, inputs) + self.biases
        
        # ReLU activation (efficient)
        self.activity = np.maximum(0, weighted)
        self.total_activations += 1
        
        return self.activity
    
    def get_activity_level(self) -> float:
        """Get average activity (for boredom detection)"""
        return np.mean(self.activity)
    
    def reinforce_active(self, learning_rate: float = 0.01):
        """Strengthen active connections (Hebbian learning)"""
        active_mask = self.activity > 0
        self.weights[active_mask] += learning_rate


class PBrain:
    """
    Complete brain-inspired neural network
    Multiple specialized regions working together
    """
    
    def __init__(self, use_sparse: bool = True):
        self.use_sparse = use_sparse
        self.regions: Dict[str, BrainRegion] = {}
        self.region_order = []
        self.global_activity = 0.0
        self.processing_count = 0
        
        # Build brain architecture
        self._build_brain()
        
        # Calculate totals
        self.total_neurons = sum(r.neuron_count for r in self.regions.values())
        self.total_connections = sum(np.sum(r.connections) for r in self.regions.values())
        
        # Emotional state (Phase 3)
        self.dopamine_level = 0.5
        self.arousal = 0.5
        self.boredom_threshold = 0.05
    
    def _build_brain(self):
        """Build the brain architecture with specialized regions"""
        
        # Sensory processing pathway
        self._add_region("sensory", 32, 16)  # Input: 16 dimensions
        self._add_region("sensory_hidden", 48, 32)
        
        # Memory and emotion pathway
        self._add_region("memory", 64, 48)
        self._add_region("emotion", 32, 64)
        
        # Language pathway (Broca's area)
        self._add_region("language", 48, 32)
        
        # Integration center
        self._add_region("integration", 64, 144)  # Combines memory + emotion + language
        
        # Reward system
        self._add_region("reward", 16, 64)
        
        # Decision making
        self._add_region("decision", 32, 80)  # Integration + reward
        
        # Motor output
        self._add_region("motor", 16, 32)
    
    def _add_region(self, name: str, neurons: int, inputs: int):
        """Add a brain region"""
        self.regions[name] = BrainRegion(name, neurons, inputs)
        self.region_order.append(name)
    
    def process(self, sensory_input: np.ndarray) -> dict:
        """
        Process input through entire brain
        Returns output and internal state
        """
        self.processing_count += 1
        
        # Sensory pathway
        sensory_out = self.regions["sensory"].activate(sensory_input)
        sensory_hidden_out = self.regions["sensory_hidden"].activate(sensory_out)
        
        # Memory pathway
        memory_out = self.regions["memory"].activate(sensory_hidden_out)
        
        # Emotion pathway
        emotion_out = self.regions["emotion"].activate(memory_out)
        
        # Language pathway
        language_out = self.regions["language"].activate(emotion_out)
        
        # Integration (combines all three)
        combined = np.concatenate([memory_out, emotion_out, language_out])
        integration_out = self.regions["integration"].activate(combined)
        
        # Reward processing
        reward_out = self.regions["reward"].activate(integration_out)
        
        # Decision making
        decision_input = np.concatenate([integration_out, reward_out])
        decision_out = self.regions["decision"].activate(decision_input)
        
        # Motor output
        motor_out = self.regions["motor"].activate(decision_out)
        
        # Update global activity
        self.global_activity = self._calculate_global_activity()
        
        # Update dopamine based on activity
        self._update_dopamine()
        
        return {
            "output": motor_out,
            "sensory": sensory_out,
            "memory": memory_out,
            "emotion": emotion_out,
            "language": language_out,
            "integration": integration_out,
            "reward": reward_out,
            "decision": decision_out,
            "global_activity": self.global_activity,
            "dopamine": self.dopamine_level,
        }
    
    def _calculate_global_activity(self) -> float:
        """Calculate overall brain activity"""
        activities = [region.get_activity_level() for region in self.regions.values()]
        return np.mean(activities)
    
    def _update_dopamine(self):
        """Update dopamine based on activity patterns"""
        # Novelty detection: high activity = novel = dopamine
        novelty_signal = max(0, self.global_activity - 0.3)
        
        # Prediction error: unexpected patterns = dopamine
        # (simplified - will be enhanced in Phase 3)
        
        # Decay dopamine slowly
        self.dopamine_level = 0.9 * self.dopamine_level + 0.1 * novelty_signal
        self.dopamine_level = np.clip(self.dopamine_level, 0.0, 1.0)
    
    def is_bored(self) -> bool:
        """Check if brain is bored (low activity)"""
        return self.global_activity < self.boredom_threshold
    
    def get_emotion_state(self) -> dict:
        """Get current emotional state from emotion region"""
        emotion_activity = self.regions["emotion"].activity
        return {
            "activity": emotion_activity,
            "dominant_emotion": np.argmax(emotion_activity),
            "intensity": np.max(emotion_activity),
        }
    
    def get_language_state(self) -> dict:
        """Get language processing state"""
        language_activity = self.regions["language"].activity
        return {
            "activity": language_activity,
            "active_units": np.sum(language_activity > 0.1),
        }
    
    def get_state_summary(self) -> dict:
        """Get complete brain state"""
        return {
            "global_activity": self.global_activity,
            "dopamine_level": self.dopamine_level,
            "processing_count": self.processing_count,
            "is_bored": self.is_bored(),
            "regions": {
                name: {
                    "activity": region.get_activity_level(),
                    "total_activations": region.total_activations,
                }
                for name, region in self.regions.items()
            }
        }
    
    def reinforce_active_regions(self, learning_rate: float = 0.01):
        """Strengthen active connections across all regions"""
        for region in self.regions.values():
            region.reinforce_active(learning_rate)


def test_pbrain():
    """Test the enhanced brain architecture"""
    print("=== P-Brain Architecture Test ===\n")
    
    # Create brain
    brain = PBrain()
    
    print(f"Brain regions: {len(brain.regions)}")
    print(f"Region order: {brain.region_order}\n")
    
    # Simulate sensory input
    sensory_input = np.random.random(16)
    
    # Process input
    print("Processing sensory input...")
    result = brain.process(sensory_input)
    
    print(f"\nGlobal activity: {result['global_activity']:.4f}")
    print(f"Dopamine level: {result['dopamine']:.4f}")
    print(f"Is bored: {brain.is_bored()}")
    
    # Region activities
    print("\nRegion activities:")
    state = brain.get_state_summary()
    for region_name, region_state in state['regions'].items():
        print(f"  {region_name:15s}: {region_state['activity']:.4f}")
    
    # Emotional state
    emotion_state = brain.get_emotion_state()
    print(f"\nEmotion intensity: {emotion_state['intensity']:.4f}")
    
    # Language state
    language_state = brain.get_language_state()
    print(f"Language active units: {language_state['active_units']}")
    
    # Process multiple inputs
    print("\n--- Processing Multiple Inputs ---")
    for i in range(10):
        input_data = np.random.random(16)
        result = brain.process(input_data)
        print(f"Input {i+1:2d}: activity={result['global_activity']:.4f}, dopamine={result['dopamine']:.4f}")
    
    # Final state
    print("\n--- Final Brain State ---")
    final_state = brain.get_state_summary()
    print(f"Total processing: {final_state['processing_count']}")
    print(f"Global activity: {final_state['global_activity']:.4f}")
    print(f"Dopamine: {final_state['dopamine_level']:.4f}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_pbrain()