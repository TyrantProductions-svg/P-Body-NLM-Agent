"""
P-Body Recursive Self-Operation
Phase 5: Self-monitoring, self-modification, metacognition, internal dialogue
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import random


class SelfOperationType(Enum):
    """Types of self-operations P-Body can perform"""
    MONITOR_STATE = "monitor"
    MODIFY_WEIGHTS = "modify_weights"
    ADJUST_PARAMETERS = "adjust_params"
    REFLECT_EMOTIONS = "reflect_emotions"
    INTERNAL_DIALOGUE = "internal_dialogue"
    METACOGNITION = "metacognition"
    CONSOLIDATE_SELF = "consolidate_self"


@dataclass
class SelfAwarenessState:
    """P-Body's current self-awareness state"""
    emotion: str = "neutral"
    emotion_intensity: float = 0.0
    dopamine_level: float = 0.5
    activity_level: float = 0.0
    memory_count: int = 0
    vocab_size: int = 0
    boredom_level: float = 0.0
    confusion_level: float = 0.0
    confidence_level: float = 0.5
    timestamp: float = 0.0


@dataclass
class InternalThought:
    """A single internal thought"""
    content: str
    emotion: str
    timestamp: float
    operation_type: SelfOperationType
    confidence: float = 0.5


class SelfMonitor:
    """Monitors P-Body's internal state"""
    
    def __init__(self):
        self.state_history: List[SelfAwarenessState] = []
        self.max_history = 100
    
    def capture_state(self, **kwargs) -> SelfAwarenessState:
        """Capture current state"""
        state = SelfAwarenessState(
            emotion=kwargs.get("emotion", "neutral"),
            emotion_intensity=kwargs.get("emotion_intensity", 0.0),
            dopamine_level=kwargs.get("dopamine_level", 0.5),
            activity_level=kwargs.get("activity_level", 0.0),
            memory_count=kwargs.get("memory_count", 0),
            vocab_size=kwargs.get("vocab_size", 0),
            boredom_level=kwargs.get("boredom_level", 0.0),
            confusion_level=kwargs.get("confusion_level", 0.0),
            confidence_level=kwargs.get("confidence_level", 0.5),
            timestamp=time.time()
        )
        
        self.state_history.append(state)
        
        # Keep history limited
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        return state
    
    def get_state_trend(self, attribute: str, window: int = 10) -> float:
        """Get trend of an attribute over recent history"""
        if len(self.state_history) < 2:
            return 0.0
        
        recent = self.state_history[-window:]
        if not hasattr(recent[0], attribute):
            return 0.0
        
        values = [getattr(s, attribute) for s in recent]
        
        # Simple linear trend
        if len(values) < 2:
            return 0.0
        
        trend = (values[-1] - values[0]) / len(values)
        return trend
    
    def detect_state_change(self, attribute: str, threshold: float = 0.2) -> bool:
        """Detect significant state change"""
        if len(self.state_history) < 2:
            return False
        
        recent = self.state_history[-1]
        previous = self.state_history[-2]
        
        if not hasattr(recent, attribute) or not hasattr(previous, attribute):
            return False
        
        current = getattr(recent, attribute)
        old = getattr(previous, attribute)
        
        return abs(current - old) > threshold
    
    def get_summary(self) -> Dict:
        """Get state summary"""
        if not self.state_history:
            return {}
        
        latest = self.state_history[-1]
        
        return {
            "current_emotion": latest.emotion,
            "emotion_intensity": latest.emotion_intensity,
            "dopamine": latest.dopamine_level,
            "activity": latest.activity_level,
            "memories": latest.memory_count,
            "vocabulary": latest.vocab_size,
            "boredom": latest.boredom_level,
            "confidence": latest.confidence_level,
            "state_changes": len(self.state_history),
        }


class SelfModifier:
    """Allows P-Body to modify her own parameters"""
    
    def __init__(self):
        self.modification_history: List[Dict] = []
        self.allowed_modifications = {
            "learning_rate": (0.001, 0.5),
            "dopamine_baseline": (0.3, 0.7),
            "memory_decay_rate": (0.01, 0.2),
            "emotion_threshold": (0.1, 0.9),
            "novelty_sensitivity": (0.1, 1.0),
        }
    
    def modify_parameter(self, param: str, new_value: float, reason: str = "") -> bool:
        """Modify a parameter if within allowed range"""
        if param not in self.allowed_modifications:
            return False
        
        min_val, max_val = self.allowed_modifications[param]
        
        if not (min_val <= new_value <= max_val):
            return False
        
        # Record modification
        mod = {
            "parameter": param,
            "old_value": None,  # Would be set by caller
            "new_value": new_value,
            "reason": reason,
            "timestamp": time.time(),
        }
        
        self.modification_history.append(mod)
        
        return True
    
    def get_modification_count(self) -> int:
        """Get total modifications made"""
        return len(self.modification_history)
    
    def get_recent_modifications(self, count: int = 5) -> List[Dict]:
        """Get recent modifications"""
        return self.modification_history[-count:]


class InternalDialogue:
    """Manages P-Body's internal thought process"""
    
    def __init__(self, max_thoughts: int = 50):
        self.thoughts: List[InternalThought] = []
        self.max_thoughts = max_thoughts
        self.thought_count = 0
    
    def add_thought(self, content: str, emotion: str, 
                   operation_type: SelfOperationType, confidence: float = 0.5):
        """Add an internal thought"""
        thought = InternalThought(
            content=content,
            emotion=emotion,
            timestamp=time.time(),
            operation_type=operation_type,
            confidence=confidence
        )
        
        self.thoughts.append(thought)
        self.thought_count += 1
        
        # Keep thoughts limited
        if len(self.thoughts) > self.max_thoughts:
            self.thoughts.pop(0)
    
    def get_recent_thoughts(self, count: int = 5) -> List[InternalThought]:
        """Get recent thoughts"""
        return self.thoughts[-count:]
    
    def get_thoughts_by_emotion(self, emotion: str) -> List[InternalThought]:
        """Get thoughts with specific emotion"""
        return [t for t in self.thoughts if t.emotion == emotion]
    
    def get_dominant_thought_emotion(self) -> str:
        """Get most common emotion in thoughts"""
        if not self.thoughts:
            return "neutral"
        
        emotion_counts = {}
        for thought in self.thoughts:
            emotion_counts[thought.emotion] = emotion_counts.get(thought.emotion, 0) + 1
        
        return max(emotion_counts, key=emotion_counts.get)
    
    def generate_self_reflection(self) -> str:
        """Generate a self-reflective thought"""
        if not self.thoughts:
            return "I have no thoughts yet."
        
        recent = self.thoughts[-3:]
        emotions = [t.emotion for t in recent]
        
        # Simple reflection based on recent thoughts
        if "bored" in emotions:
            return "I feel bored. I should seek new information."
        elif "confused" in emotions:
            return "I'm confused. I need to process this more carefully."
        elif "happy" in emotions:
            return "I feel good. Learning is working well."
        elif "fear" in emotions:
            return "I'm cautious. This feels unfamiliar."
        else:
            return f"I'm thinking about {len(self.thoughts)} things."


class Metacognition:
    """Thinking about thinking - P-Body's self-awareness"""
    
    def __init__(self):
        self.self_model: Dict = {
            "capabilities": [],
            "limitations": [],
            "preferences": [],
            "emotional_patterns": {},
        }
        self.insights: List[str] = []
    
    def analyze_self(self, state: SelfAwarenessState, 
                    recent_thoughts: List[InternalThought]) -> Dict:
        """Analyze current self-state"""
        analysis = {
            "emotion_stability": self._calculate_emotion_stability(recent_thoughts),
            "learning_efficiency": self._estimate_learning_efficiency(state),
            "self_awareness_level": self._calculate_awareness_level(state),
            "cognitive_load": self._estimate_cognitive_load(state),
        }
        
        return analysis
    
    def generate_insight(self, analysis: Dict) -> Optional[str]:
        """Generate insight from self-analysis"""
        insights = []
        
        if analysis.get("emotion_stability", 1.0) < 0.3:
            insights.append("My emotions are fluctuating rapidly.")
        
        if analysis.get("learning_efficiency", 1.0) < 0.3:
            insights.append("I'm not learning effectively right now.")
        
        if analysis.get("cognitive_load", 0.0) > 0.8:
            insights.append("I'm processing too much at once.")
        
        if analysis.get("self_awareness_level", 0.0) > 0.7:
            insights.append("I'm highly aware of my current state.")
        
        if insights:
            insight = random.choice(insights)
            self.insights.append(insight)
            return insight
        
        return None
    
    def _calculate_emotion_stability(self, thoughts: List[InternalThought]) -> float:
        """Calculate how stable emotions are"""
        if len(thoughts) < 2:
            return 1.0
        
        emotions = [t.emotion for t in thoughts]
        unique = len(set(emotions))
        
        # Fewer unique emotions = more stable
        return 1.0 - (unique / len(emotions))
    
    def _estimate_learning_efficiency(self, state: SelfAwarenessState) -> float:
        """Estimate how well P-Body is learning"""
        # Simple heuristic
        if state.activity_level > 0.5 and state.dopamine_level > 0.5:
            return 0.8
        elif state.activity_level > 0.3:
            return 0.5
        else:
            return 0.2
    
    def _calculate_awareness_level(self, state: SelfAwarenessState) -> float:
        """Calculate self-awareness level"""
        # Based on confidence and emotion intensity
        return (state.confidence_level + state.emotion_intensity) / 2
    
    def _estimate_cognitive_load(self, state: SelfAwarenessState) -> float:
        """Estimate cognitive load"""
        # Based on activity and memory count
        activity_factor = state.activity_level
        memory_factor = min(1.0, state.memory_count / 100)
        
        return (activity_factor + memory_factor) / 2


class RecursiveSystem:
    """
    Main recursive self-operation system
    Integrates self-monitoring, modification, dialogue, and metacognition
    CONNECTED to brain, memory, biological, and language systems
    """
    
    def __init__(self, brain=None, memory=None, biological=None, language=None):
        self.monitor = SelfMonitor()
        self.modifier = SelfModifier()
        self.dialogue = InternalDialogue()
        self.metacognition = Metacognition()
        
        # Connected systems
        self.brain = brain
        self.memory = memory
        self.biological = biological
        self.language = language
        
        self.operation_count = 0
        self.last_operation_time = 0.0
    
    def capture_system_state(self) -> SelfAwarenessState:
        """Capture actual state from all connected systems"""
        state = SelfAwarenessState(timestamp=time.time())
        
        # From brain
        if self.brain:
            try:
                brain_state = self.brain.get_state_summary()
                if brain_state:
                    state.activity_level = brain_state.get("global_activity", 0.0)
                    state.dopamine_level = brain_state.get("dopamine_level", 0.5)
                    state.confidence_level = min(1.0, brain_state.get("global_activity", 0.0) / 2.0)
            except Exception:
                pass  # Brain not ready, use defaults
        
        # From biological
        if self.biological:
            try:
                bio_state = self.biological.get_state()
                if bio_state and "emotion" in bio_state:
                    emotion_data = bio_state["emotion"]
                    if isinstance(emotion_data, dict):
                        state.emotion = emotion_data.get("current_emotion", "neutral")
                    else:
                        state.emotion = "neutral"
                
                # Get emotion intensity safely
                if hasattr(self.biological, "emotions"):
                    if hasattr(self.biological.emotions, "emotion_intensity"):
                        state.emotion_intensity = self.biological.emotions.emotion_intensity
                    
                    # Get dopamine level safely
                    if hasattr(self.biological.emotions, "dopamine"):
                        if hasattr(self.biological.emotions.dopamine, "get_level"):
                            state.dopamine_level = self.biological.emotions.dopamine.get_level()
                    
                    # Get boredom threshold
                    if hasattr(self.biological.emotions, "boredom_threshold"):
                        state.boredom_level = self.biological.emotions.boredom_threshold
            except Exception:
                pass  # Biological not ready, use defaults
        
        # From memory
        if self.memory:
            try:
                if hasattr(self.memory, "stm") and hasattr(self.memory.stm, "memories"):
                    stm_count = len(self.memory.stm.memories)
                else:
                    stm_count = 0
                
                if hasattr(self.memory, "ltm") and hasattr(self.memory.ltm, "get_memory_count"):
                    ltm_count = self.memory.ltm.get_memory_count()
                else:
                    ltm_count = 0
                
                state.memory_count = stm_count + ltm_count
            except Exception:
                pass  # Memory not ready, use defaults
        
        # From language
        if self.language:
            try:
                if hasattr(self.language, "vocab") and hasattr(self.language.vocab, "get_size"):
                    state.vocab_size = self.language.vocab.get_size()
            except Exception:
                pass  # Language not ready, use defaults
        
        return state
    
    def self_monitor(self, **kwargs) -> SelfAwarenessState:
        """Monitor own state - pulls from connected systems"""
        # Capture from systems first, then override with kwargs
        state = self.capture_system_state()
        
        # Allow manual overrides
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        
        # Record in history
        self.monitor.capture_state(
            emotion=state.emotion,
            emotion_intensity=state.emotion_intensity,
            dopamine_level=state.dopamine_level,
            activity_level=state.activity_level,
            memory_count=state.memory_count,
            vocab_size=state.vocab_size,
            boredom_level=state.boredom_level,
            confusion_level=state.confusion_level,
            confidence_level=state.confidence_level,
        )
        
        # Add thought about monitoring
        self.dialogue.add_thought(
            content=f"Monitoring: emotion={state.emotion}, activity={state.activity_level:.2f}, dopamine={state.dopamine_level:.2f}",
            emotion=state.emotion,
            operation_type=SelfOperationType.MONITOR_STATE,
            confidence=state.confidence_level
        )
        
        self.operation_count += 1
        return state
    
    def apply_modification(self, param: str, value: float, reason: str = "") -> bool:
        """Actually modify connected systems"""
        success = self.modifier.modify_parameter(param, value, reason)
        
        if not success:
            return False
        
        # Apply to brain
        if self.brain:
            if param == "learning_rate":
                self.brain.reinforce_active_regions(learning_rate=value)
            elif param == "dopamine_baseline":
                self.brain.dopamine_level = value
        
        # Apply to memory
        if self.memory:
            if param == "memory_decay_rate":
                self.memory.stm.decay_all(rate=value)
        
        # Apply to biological
        if self.biological:
            try:
                if param == "emotion_threshold":
                    if hasattr(self.biological.emotions, "boredom_threshold"):
                        self.biological.emotions.boredom_threshold = value
                elif param == "novelty_sensitivity":
                    if hasattr(self.biological.emotions, "dopamine"):
                        if hasattr(self.biological.emotions.dopamine, "novelty_weight"):
                            self.biological.emotions.dopamine.novelty_weight = value
            except Exception:
                pass  # Biological modification failed, but modification was recorded
        
        if success:
            self.dialogue.add_thought(
                content=f"Modified {param} to {value}: {reason}",
                emotion="curious",
                operation_type=SelfOperationType.MODIFY_WEIGHTS,
                confidence=0.7
            )
        
        self.operation_count += 1
        return success
    
    def self_modify(self, param: str, value: float, reason: str = "") -> bool:
        """Modify own parameters - alias for apply_modification"""
        return self.apply_modification(param, value, reason)
    
    def self_reflect(self) -> str:
        """Generate self-reflection"""
        reflection = self.dialogue.generate_self_reflection()
        
        # Safely get emotion from history
        if self.monitor.state_history:
            emotion = self.monitor.state_history[-1].emotion
        else:
            emotion = "neutral"
        
        self.dialogue.add_thought(
            content=reflection,
            emotion=emotion,
            operation_type=SelfOperationType.REFLECT_EMOTIONS,
            confidence=0.6
        )
        
        self.operation_count += 1
        return reflection
    
    def metacognitive_analysis(self) -> Dict:
        """Perform metacognitive analysis"""
        if not self.monitor.state_history:
            return {
                "analysis": {
                    "emotion_stability": 1.0,
                    "learning_efficiency": 0.5,
                    "self_awareness_level": 0.0,
                    "cognitive_load": 0.0,
                },
                "insight": "No state history yet. I'm just starting to understand myself.",
            }
        
        state = self.monitor.state_history[-1]
        recent_thoughts = self.dialogue.get_recent_thoughts(5)
        
        analysis = self.metacognition.analyze_self(state, recent_thoughts)
        insight = self.metacognition.generate_insight(analysis)
        
        if insight:
            self.dialogue.add_thought(
                content=insight,
                emotion="curious",
                operation_type=SelfOperationType.METACOGNITION,
                confidence=0.8
            )
        
        self.operation_count += 1
        
        return {
            "analysis": analysis,
            "insight": insight,
        }
    
    def internal_dialogue_loop(self, iterations: int = 3) -> List[str]:
        """Run internal dialogue loop"""
        thoughts = []
        
        for i in range(iterations):
            # Monitor state
            if self.monitor.state_history:
                state = self.monitor.state_history[-1]
                
                # Generate thought based on state
                if state.boredom_level > 0.7:
                    thought = "I'm bored. I need stimulation."
                    emotion = "bored"
                elif state.dopamine_level > 0.7:
                    thought = "I feel rewarded. Learning is going well."
                    emotion = "happy"
                elif state.confusion_level > 0.5:
                    thought = "I'm confused. Need to process more."
                    emotion = "confused"
                else:
                    thought = f"Processing... (cycle {i+1})"
                    emotion = "neutral"
                
                self.dialogue.add_thought(
                    content=thought,
                    emotion=emotion,
                    operation_type=SelfOperationType.INTERNAL_DIALOGUE,
                    confidence=0.5
                )
                
                thoughts.append(thought)
            else:
                # No state history yet - generate default thoughts
                thought = f"Initializing... (cycle {i+1})"
                self.dialogue.add_thought(
                    content=thought,
                    emotion="neutral",
                    operation_type=SelfOperationType.INTERNAL_DIALOGUE,
                    confidence=0.5
                )
                thoughts.append(thought)
        
        self.operation_count += iterations
        return thoughts
    
    def get_recursive_state(self) -> Dict:
        """Get complete recursive system state"""
        return {
            "monitor_summary": self.monitor.get_summary(),
            "modifications": self.modifier.get_modification_count(),
            "thought_count": self.dialogue.thought_count,
            "dominant_thought_emotion": self.dialogue.get_dominant_thought_emotion(),
            "insights": len(self.metacognition.insights),
            "total_operations": self.operation_count,
        }