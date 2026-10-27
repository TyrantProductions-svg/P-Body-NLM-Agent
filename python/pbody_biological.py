"""
P-Body Biological Processes
Phase 3: Dopamine system, emotional states, sleep optimization, emotion-driven processing, expressions
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time


# ==================== EXPRESSION SYSTEM ====================

class EyeType(Enum):
    OPEN = "open"
    HALF_SHUT = "half_shut"
    CLOSED = "closed"
    WIDE = "wide"
    SQUINT = "squint"


class MouthType(Enum):
    NORMAL = "normal"
    SMILE = "smile"
    SMIRK = "smirk"
    FROWN = "frown"
    OPEN = "open"
    TIGHT = "tight"


EXPRESSION_MAP = {
    "happy": (EyeType.OPEN, MouthType.SMILE),
    "teasing": (EyeType.HALF_SHUT, MouthType.SMIRK),
    "sleeping": (EyeType.CLOSED, MouthType.NORMAL),
    "fear": (EyeType.WIDE, MouthType.OPEN),
    "disgust": (EyeType.SQUINT, MouthType.TIGHT),
    "neutral": (EyeType.OPEN, MouthType.NORMAL),
    "cautious": (EyeType.HALF_SHUT, MouthType.NORMAL),
    "bored": (EyeType.HALF_SHUT, MouthType.FROWN),
    "curious": (EyeType.WIDE, MouthType.NORMAL),
    "excited": (EyeType.WIDE, MouthType.SMILE),
}


class ExpressionController:
    """Controls LED matrix expressions based on emotional state"""
    
    def __init__(self):
        self.current_emotion = "neutral"
        self.current_eyes = EyeType.OPEN
        self.current_mouth = MouthType.NORMAL
        self.expression_history = []
    
    def set_emotion(self, emotion: str):
        """Set emotion and update expression"""
        self.current_emotion = emotion
        
        if emotion in EXPRESSION_MAP:
            eyes, mouth = EXPRESSION_MAP[emotion]
            self.current_eyes = eyes
            self.current_mouth = mouth
            
            self.expression_history.append({
                "emotion": emotion,
                "eyes": eyes.value,
                "mouth": mouth.value
            })
        
        return self.current_eyes, self.current_mouth
    
    def get_command(self) -> dict:
        """Get command to send to microcontroller"""
        return {
            "eyes": self.current_eyes.value,
            "mouth": self.current_mouth.value,
            "emotion": self.current_emotion
        }
    
    def create_custom_expression(self, eyes: EyeType, mouth: MouthType):
        """Create custom expression"""
        self.current_eyes = eyes
        self.current_mouth = mouth
        self.expression_history.append({
            "emotion": "custom",
            "eyes": eyes.value,
            "mouth": mouth.value
        })
        return eyes, mouth


# ==================== EMOTIONAL STATES ====================

class EmotionalState(Enum):
    """Emotional states with behavioral effects"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    BORED = "bored"
    FEAR = "fear"
    DISGUST = "disgust"
    CAUTIOUS = "cautious"
    CURIOUS = "curious"
    EXCITED = "excited"


@dataclass
class EmotionProfile:
    """Defines how each emotion affects processing"""
    name: str
    learning_rate_modifier: float = 1.0  # Multiplier for learning
    activity_threshold: float = 0.0  # Minimum activity to trigger
    dopamine_modifier: float = 0.0  # Affects dopamine release
    novelty_sensitivity: float = 1.0  # How sensitive to new patterns
    memory_consolidation_rate: float = 1.0  # How fast memories consolidate


# Emotion profiles
EMOTION_PROFILES = {
    EmotionalState.NEUTRAL: EmotionProfile(
        name="neutral",
        learning_rate_modifier=1.0,
        activity_threshold=0.0,
        dopamine_modifier=0.0,
        novelty_sensitivity=1.0,
        memory_consolidation_rate=1.0,
    ),
    EmotionalState.HAPPY: EmotionProfile(
        name="happy",
        learning_rate_modifier=1.3,  # Learn faster when happy
        activity_threshold=0.3,
        dopamine_modifier=0.2,  # More dopamine
        novelty_sensitivity=1.2,
        memory_consolidation_rate=1.5,  # Better memory consolidation
    ),
    EmotionalState.BORED: EmotionProfile(
        name="bored",
        learning_rate_modifier=0.8,
        activity_threshold=0.0,
        dopamine_modifier=-0.1,  # Less dopamine
        novelty_sensitivity=1.5,  # More sensitive to novelty (seeks stimulation)
        memory_consolidation_rate=0.7,
    ),
    EmotionalState.FEAR: EmotionProfile(
        name="fear",
        learning_rate_modifier=1.5,  # Learn fast from threats
        activity_threshold=0.4,
        dopamine_modifier=-0.3,  # Less dopamine (stress)
        novelty_sensitivity=2.0,  # Hyper-vigilant
        memory_consolidation_rate=2.0,  # Strong fear memories
    ),
    EmotionalState.DISGUST: EmotionProfile(
        name="disgust",
        learning_rate_modifier=0.5,  # Avoid learning disgusting things
        activity_threshold=0.2,
        dopamine_modifier=-0.2,
        novelty_sensitivity=0.5,  # Reject novel patterns
        memory_consolidation_rate=1.2,
    ),
    EmotionalState.CAUTIOUS: EmotionProfile(
        name="cautious",
        learning_rate_modifier=0.9,
        activity_threshold=0.1,
        dopamine_modifier=-0.05,
        novelty_sensitivity=1.3,  # Carefully evaluate novelty
        memory_consolidation_rate=1.1,
    ),
    EmotionalState.CURIOUS: EmotionProfile(
        name="curious",
        learning_rate_modifier=1.4,  # Very eager to learn
        activity_threshold=0.2,
        dopamine_modifier=0.15,
        novelty_sensitivity=1.8,  # Loves novelty
        memory_consolidation_rate=1.3,
    ),
    EmotionalState.EXCITED: EmotionProfile(
        name="excited",
        learning_rate_modifier=1.5,
        activity_threshold=0.5,
        dopamine_modifier=0.3,  # High dopamine
        novelty_sensitivity=1.6,
        memory_consolidation_rate=1.8,
    ),
}


class DopamineSystem:
    """
    Dopamine reward system
    Triggers from information processing, not user interaction
    """
    
    def __init__(self, baseline: float = 0.5):
        self.baseline = baseline
        self.current_level = baseline
        self.history: List[float] = []
        
        # Dopamine triggers
        self.novelty_reward = 0.1  # Reward for new patterns
        self.prediction_reward = 0.15  # Reward for correct predictions
        self.coherence_reward = 0.05  # Reward for consistent information
        self.decay_rate = 0.1  # How fast dopamine returns to baseline
    
    def process_novelty(self, novelty_score: float) -> float:
        """Reward for encountering novel patterns"""
        reward = novelty_score * self.novelty_reward
        self.current_level += reward
        self._record()
        return reward
    
    def process_prediction(self, prediction_accuracy: float) -> float:
        """Reward for successful predictions"""
        reward = prediction_accuracy * self.prediction_reward
        self.current_level += reward
        self._record()
        return reward
    
    def process_coherence(self, coherence_score: float) -> float:
        """Reward for information consistency"""
        reward = coherence_score * self.coherence_reward
        self.current_level += reward
        self._record()
        return reward
    
    def decay(self):
        """Return dopamine to baseline"""
        diff = self.current_level - self.baseline
        self.current_level -= diff * self.decay_rate
        self.current_level = np.clip(self.current_level, 0.0, 1.0)
        self._record()
    
    def get_level(self) -> float:
        """Get current dopamine level"""
        return self.current_level
    
    def _record(self):
        """Record dopamine level"""
        self.history.append(self.current_level)
        if len(self.history) > 100:
            self.history.pop(0)
    
    def get_average(self) -> float:
        """Get average dopamine level"""
        return np.mean(self.history) if self.history else self.baseline


class EmotionalProcessor:
    """
    Manages emotional states and their effects on processing
    """
    
    def __init__(self):
        self.current_emotion = EmotionalState.NEUTRAL
        self.emotion_intensity = 0.0
        self.emotion_history: List[Dict] = []
        self.dopamine = DopamineSystem()
        
        # Activity tracking for boredom
        self.recent_activities: List[float] = []
        self.boredom_threshold = 0.1
        self.activity_window = 10
    
    def update_emotion(self, brain_activity: float, novelty_score: float, 
                      prediction_accuracy: float) -> EmotionalState:
        """
        Determine emotional state based on brain activity and processing
        """
        # Track activity
        self.recent_activities.append(brain_activity)
        if len(self.recent_activities) > self.activity_window:
            self.recent_activities.pop(0)
        
        avg_activity = np.mean(self.recent_activities)
        
        # Process dopamine triggers
        self.dopamine.process_novelty(novelty_score)
        self.dopamine.process_prediction(prediction_accuracy)
        self.dopamine.decay()
        
        dopamine_level = self.dopamine.get_level()
        
        # Determine emotion
        new_emotion = self._determine_emotion(avg_activity, novelty_score, dopamine_level)
        
        if new_emotion != self.current_emotion:
            self.current_emotion = new_emotion
            self.emotion_intensity = self._calculate_intensity(
                avg_activity, novelty_score, dopamine_level
            )
            
            # Record emotion change
            self.emotion_history.append({
                "emotion": new_emotion.value,
                "intensity": self.emotion_intensity,
                "activity": avg_activity,
                "dopamine": dopamine_level,
                "timestamp": time.time(),
            })
        
        return self.current_emotion
    
    def _determine_emotion(self, activity: float, novelty: float, 
                          dopamine: float) -> EmotionalState:
        """Determine current emotional state"""
        
        # Fear: high activity + low dopamine (threat detection)
        if activity > 0.5 and dopamine < 0.3:
            return EmotionalState.FEAR
        
        # Excited: high activity + high dopamine
        if activity > 0.4 and dopamine > 0.7:
            return EmotionalState.EXCITED
        
        # Happy: moderate-high activity + moderate-high dopamine
        if activity > 0.25 and dopamine > 0.5:
            return EmotionalState.HAPPY
        
        # Curious: moderate activity + high novelty
        if activity > 0.15 and novelty > 0.6:
            return EmotionalState.CURIOUS
        
        # Cautious: moderate activity + moderate dopamine
        if activity > 0.1 and 0.3 < dopamine < 0.6:
            return EmotionalState.CAUTIOUS
        
        # Disgust: very low novelty + low dopamine
        if novelty < 0.05 and dopamine < 0.35:
            return EmotionalState.DISGUST
        
        # Boredom: very low activity
        if activity < self.boredom_threshold:
            return EmotionalState.BORED
        
        # Default: neutral
        return EmotionalState.NEUTRAL
    
    def _calculate_intensity(self, activity: float, novelty: float, 
                            dopamine: float) -> float:
        """Calculate emotion intensity (0-1)"""
        return np.clip((activity + novelty + dopamine) / 3.0, 0.0, 1.0)
    
    def get_profile(self) -> EmotionProfile:
        """Get current emotion's processing profile"""
        return EMOTION_PROFILES[self.current_emotion]
    
    def get_learning_rate(self, base_rate: float = 0.01) -> float:
        """Get emotion-modified learning rate"""
        profile = self.get_profile()
        return base_rate * profile.learning_rate_modifier
    
    def is_bored(self) -> bool:
        """Check if currently bored"""
        return self.current_emotion == EmotionalState.BORED
    
    def get_state(self) -> Dict:
        """Get current emotional state"""
        return {
            "emotion": self.current_emotion.value,
            "intensity": self.emotion_intensity,
            "dopamine_level": self.dopamine.get_level(),
            "dopamine_average": self.dopamine.get_average(),
            "avg_activity": np.mean(self.recent_activities) if self.recent_activities else 0.0,
        }


class SleepOptimizer:
    """
    Sleep cycle optimization
    Consolidates memories, updates weights, prunes unimportant data
    """
    
    def __init__(self):
        self.sleep_count = 0
        self.total_consolidated = 0
        self.total_pruned = 0
    
    def sleep_cycle(self, memory_system, brain, emotion_processor):
        """
        Execute sleep cycle
        - Consolidate important memories
        - Update weights based on emotion-modified learning
        - Prune unimportant memories/connections
        """
        self.sleep_count += 1
        
        print(f"\n{'='*60}")
        print(f"[Sleep] Cycle #{self.sleep_count} starting...")
        print(f"{'='*60}")
        
        # Get emotion profile for sleep parameters
        profile = emotion_processor.get_profile()
        
        # Phase 1: Memory consolidation
        print("\n[Sleep] Phase 1: Memory consolidation")
        important_memories = memory_system.stm.get_important_memories()
        
        consolidation_rate = profile.memory_consolidation_rate
        consolidated_count = int(len(important_memories) * consolidation_rate)
        
        for i, memory in enumerate(important_memories[:consolidated_count]):
            memory_system.ltm.store(memory)
            self.total_consolidated += 1
        
        print(f"  Consolidated {consolidated_count}/{len(important_memories)} memories")
        
        # Phase 2: Weight optimization
        print("\n[Sleep] Phase 2: Weight optimization")
        learning_rate = emotion_processor.get_learning_rate(0.01)
        brain.reinforce_active_regions(learning_rate)
        print(f"  Learning rate: {learning_rate:.4f}")
        
        # Phase 3: Pruning
        print("\n[Sleep] Phase 3: Pruning")
        memory_system.stm.decay_all(rate=0.3)
        pruned = len([m for m in memory_system.stm.memories if m.importance < 0.1])
        self.total_pruned += pruned
        print(f"  Pruned {pruned} low-importance memories")
        
        # Phase 4: Clear STM
        print("\n[Sleep] Phase 4: Clearing short-term memory")
        memory_system.stm.clear()
        
        # Phase 5: Dopamine reset
        print("\n[Sleep] Phase 5: Dopamine reset")
        emotion_processor.dopamine.current_level = emotion_processor.dopamine.baseline
        print(f"  Dopamine reset to baseline: {emotion_processor.dopamine.baseline}")
        
        print(f"\n[Sleep] Cycle #{self.sleep_count} complete")
        print(f"  Total consolidated: {self.total_consolidated}")
        print(f"  Total pruned: {self.total_pruned}")
        print(f"{'='*60}\n")
    
    def get_stats(self) -> Dict:
        """Get sleep optimization statistics"""
        return {
            "sleep_count": self.sleep_count,
            "total_consolidated": self.total_consolidated,
            "total_pruned": self.total_pruned,
        }


class BiologicalSystem:
    """
    Complete biological processes integration
    Combines dopamine, emotions, and sleep
    """
    
    def __init__(self):
        self.emotions = EmotionalProcessor()
        self.sleep = SleepOptimizer()
        self.expressions = ExpressionController()
    
    def process_experience(self, brain, memory_system, sensory_input, 
                          novelty_score=0.5, prediction_accuracy=0.5):
        """
        Process a complete experience with biological systems
        """
        # Process through brain
        brain_result = brain.process(sensory_input)
        
        # Update emotions
        emotion = self.emotions.update_emotion(
            brain_result['global_activity'],
            novelty_score,
            prediction_accuracy
        )
        
        # Add to memory with emotion tag
        memory_system.experience(
            sensory_input.tolist() if hasattr(sensory_input, 'tolist') else list(sensory_input),
            emotion=emotion.value
        )
        
        # Update expression
        self.expressions.set_emotion(emotion.value)
        
        return {
            "brain": brain_result,
            "emotion": emotion.value,
            "emotion_intensity": self.emotions.emotion_intensity,
            "dopamine": self.emotions.dopamine.get_level(),
            "expression": self.expressions.get_command(),
        }
    
    def sleep_cycle(self, memory_system, brain):
        """Execute sleep cycle"""
        self.sleep.sleep_cycle(memory_system, brain, self.emotions)
    
    def get_state(self) -> Dict:
        """Get complete biological state"""
        return {
            "emotion": self.emotions.get_state(),
            "sleep": self.sleep.get_stats(),
        }


def test_biological_system():
    """Test the biological processes"""
    from pbrain import PBrain
    from pbody_memory import MemorySystem
    
    print("=== P-Body Biological Processes Test ===\n")
    
    # Initialize systems
    brain = PBrain()
    memory = MemorySystem()
    bio = BiologicalSystem()
    
    # Simulate experiences
    print("--- Processing Experiences ---")
    for i in range(15):
        # Generate sensory input
        sensory_input = np.random.random(16)
        
        # Vary novelty and prediction
        novelty = np.random.random()
        prediction = np.random.random()
        
        # Process
        result = bio.process_experience(
            brain, memory, sensory_input,
            novelty_score=novelty,
            prediction_accuracy=prediction
        )
        
        print(f"Exp {i+1:2d}: {result['emotion']:10s} (intensity: {result['emotion_intensity']:.3f}, "
              f"dopamine: {result['dopamine']:.3f})")
    
    # Sleep cycle
    print("\n--- Sleep Cycle ---")
    bio.sleep_cycle(memory, brain)
    
    # Post-sleep experiences
    print("\n--- Post-Sleep Experiences ---")
    for i in range(5):
        sensory_input = np.random.random(16)
        result = bio.process_experience(brain, memory, sensory_input)
        print(f"Exp {i+1:2d}: {result['emotion']:10s} (intensity: {result['emotion_intensity']:.3f})")
    
    # Final state
    print("\n--- Final Biological State ---")
    state = bio.get_state()
    print(f"Current emotion: {state['emotion']['emotion']}")
    print(f"Dopamine level: {state['emotion']['dopamine_level']:.3f}")
    print(f"Sleep cycles: {state['sleep']['sleep_count']}")
    print(f"Memories consolidated: {state['sleep']['total_consolidated']}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_biological_system()