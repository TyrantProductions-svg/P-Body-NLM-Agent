"""
P-Body Main Integration Controller
Phase 7: Integrates all systems into one cohesive entity
Includes Basal Ganglia communication (microcontroller coordination)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import time
import json
import numpy as np

# Import all P-Body systems
from pbrain import PBrain
from pbody_memory import MemorySystem
from pbody_biological import BiologicalSystem, EmotionalState
from pbody_language import BrocasArea
from pbody_recursive import RecursiveSystem


@dataclass
class PBodyState:
    """Complete state of P-Body"""
    brain_activity: float = 0.0
    brain_dopamine: float = 0.5
    current_emotion: str = "neutral"
    emotion_intensity: float = 0.0
    dopamine_level: float = 0.5
    is_bored: bool = False
    stm_count: int = 0
    ltm_count: int = 0
    sleep_cycles: int = 0
    vocab_size: int = 0
    context_size: int = 0
    language_activity: float = 0.0
    thought_count: int = 0
    modifications: int = 0
    is_sleeping: bool = False
    uptime: float = 0.0
    total_inputs: int = 0


class BasalGangliaBridge:
    """
    Bridge between Python (Dragonwing) and Basal Ganglia (microcontroller)
    Handles serial communication and command translation
    """
    
    def __init__(self, port: Optional[str] = None, baud: int = 115200):
        self.port = port
        self.baud = baud
        self.serial = None
        self.connected = False
        self.command_queue: List[str] = []
        
        # Try to connect if port specified
        if port:
            self.connect(port, baud)
    
    def connect(self, port: str, baud: int = 115200):
        """Connect to microcontroller via serial"""
        try:
            import serial
            self.serial = serial.Serial(port, baud, timeout=1)
            self.connected = True
            print(f"[Basal Ganglia] Connected to {port}")
        except Exception as e:
            print(f"[Basal Ganglia] Connection failed: {e}")
            self.connected = False
    
    def send_command(self, command: str):
        """Send command to basal ganglia"""
        self.command_queue.append(command)
        
        if self.connected and self.serial:
            try:
                self.serial.write(f"{command}\n".encode())
                print(f"[Basal Ganglia] Sent: {command}")
            except Exception as e:
                print(f"[Basal Ganglia] Send failed: {e}")
    
    def send_expression(self, emotion: str):
        """Send expression command"""
        self.send_command(f"expression:{emotion}")
    
    def send_sleep(self):
        """Send sleep command"""
        self.send_command("sleep")
    
    def send_wake(self):
        """Send wake command"""
        self.send_command("wake")
    
    def send_status_request(self):
        """Request status from basal ganglia"""
        self.send_command("status")
    
    def send_input(self, input_vec: List[float]):
        """Send neural input vector"""
        input_str = ",".join(f"{v:.4f}" for v in input_vec)
        self.send_command(f"input:{input_str}")
    
    def read_response(self) -> Optional[str]:
        """Read response from basal ganglia"""
        if self.connected and self.serial and self.serial.in_waiting > 0:
            try:
                return self.serial.readline().decode().strip()
            except Exception:
                return None
        return None
    
    def process_queue(self):
        """Process all queued commands"""
        for cmd in self.command_queue:
            print(f"[Queue] {cmd}")
        self.command_queue.clear()
    
    def disconnect(self):
        """Disconnect from microcontroller"""
        if self.serial:
            self.serial.close()
            self.connected = False
            print("[Basal Ganglia] Disconnected")


class PBodyIntegration:
    """
    Main P-Body controller
    Integrates all systems into one cohesive entity
    """
    
    def __init__(self, name: str = "P-Body", serial_port: Optional[str] = None):
        self.name = name
        self.start_time = time.time()
        
        # Initialize all systems
        self.brain = PBrain()
        self.memory = MemorySystem()
        self.biological = BiologicalSystem()
        self.language = BrocasArea()
        self.recursive = RecursiveSystem(
            brain=self.brain,
            memory=self.memory,
            biological=self.biological,
            language=self.language
        )
        
        # Basal ganglia bridge
        self.basal_ganglia = BasalGangliaBridge(port=serial_port)
        
        # Integration state
        self.state = PBodyState()
        self.input_history: List[Dict] = []
        
        # Communication buffer (for dual-chip)
        self.microcontroller_commands: List[Dict] = []
        
        print(f"[{self.name}] Initialized")
        print(f"[{self.name}] Systems: Brain, Memory, Biological, Language, Recursive, Basal Ganglia")
    
    def process_input(self, text: str, emotion: str = "neutral") -> Dict:
        """Process a complete input through all systems"""
        self.state.total_inputs += 1
        
        # 1. Language processing (Broca's area)
        lang_result = self.language.process_input(text, emotion)
        
        # 2. Convert text to brain input
        brain_input = self._text_to_brain_input(text)
        
        # 3. Process through biological system
        bio_result = self.biological.process_experience(
            brain=self.brain,
            memory_system=self.memory,
            sensory_input=np.array(brain_input),
            novelty_score=0.5,
            prediction_accuracy=0.5
        )
        
        # 4. Memory storage (already done in biological, but reinforce)
        if self.memory.stm.current_focus:
            self.memory.stm.current_focus.reinforce()
        
        # 5. Recursive self-monitoring
        current_emotion = bio_result.get("emotion", emotion)
        self.recursive.self_monitor(
            emotion=current_emotion,
            emotion_intensity=bio_result.get("emotion_intensity", 0.0),
            dopamine_level=bio_result.get("dopamine", 0.5),
            activity_level=self.brain.global_activity,
            memory_count=len(self.memory.stm.memories),
            vocab_size=self.language.vocab.get_size(),
            boredom_level=1.0 - self.brain.global_activity,
            confidence_level=0.5
        )
        
        # 6. Generate microcontroller commands
        self._generate_microcontroller_commands()
        
        # 7. Send to basal ganglia
        self._send_to_basal_ganglia(current_emotion, brain_input)
        
        # 8. Update state
        self._update_state()
        
        # 9. Record input
        self.input_history.append({
            "text": text,
            "emotion": emotion,
            "timestamp": time.time(),
            "result": bio_result
        })
        
        return {
            "processed": True,
            "emotion": current_emotion,
            "expression": {
                "eyes": self.biological.expressions.current_eyes.value,
                "mouth": self.biological.expressions.current_mouth.value,
                "emotion": self.biological.expressions.current_emotion,
            },
            "brain_activity": self.brain.global_activity,
            "dopamine": bio_result.get("dopamine", 0.5),
        }
    
    def sleep(self) -> Dict:
        """Run complete sleep cycle"""
        self.state.is_sleeping = True
        
        print(f"\n[{self.name}] Going to sleep...")
        
        # 1. Expression: sleeping face
        self.biological.expressions.set_emotion("sleeping")
        self._generate_microcontroller_commands()
        
        # 2. Send sleep command to basal ganglia
        self.basal_ganglia.send_sleep()
        
        # 3. Memory consolidation
        sleep_result = self.memory.sleep_consolidate()
        
        # 4. Clear language context
        self.language.clear_context()
        
        # 5. Recursive self-reflection
        self.recursive.self_reflect()
        
        # 6. Update state
        self.state.sleep_cycles += 1
        self.state.is_sleeping = False
        self._update_state()
        
        # 7. Send wake command to basal ganglia
        self.basal_ganglia.send_wake()
        
        print(f"[{self.name}] Woke up after sleep cycle")
        
        return {
            "sleep_cycles": self.state.sleep_cycles,
            "memories_consolidated": sleep_result.get("consolidated", 0),
            "memories_pruned": sleep_result.get("pruned", 0),
            "expression": {
                "eyes": self.biological.expressions.current_eyes.value,
                "mouth": self.biological.expressions.current_mouth.value,
                "emotion": self.biological.expressions.current_emotion,
            },
        }
    
    def get_response(self) -> str:
        """Generate a response based on current state"""
        if self.language.context.is_empty():
            return ""
        
        return self.language.generate_response(max_length=10)
    
    def self_reflect(self) -> Dict:
        """Run self-reflection cycle"""
        analysis = self.recursive.metacognitive_analysis()
        thoughts = self.recursive.internal_dialogue_loop(iterations=3)
        reflection = self.recursive.self_reflect()
        
        return {
            "analysis": analysis,
            "thoughts": thoughts,
            "reflection": reflection,
            "state": self.recursive.get_recursive_state(),
        }
    
    def get_state(self) -> PBodyState:
        """Get complete P-Body state"""
        self._update_state()
        return self.state
    
    def get_microcontroller_commands(self) -> List[Dict]:
        """Get pending commands for microcontroller"""
        commands = self.microcontroller_commands.copy()
        self.microcontroller_commands.clear()
        return commands
    
    def get_basal_ganglia_status(self) -> Optional[Dict]:
        """Get status from basal ganglia"""
        self.basal_ganglia.send_status_request()
        response = self.basal_ganglia.read_response()
        
        if response:
            try:
                # Parse status response
                lines = response.split('\n')
                status = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in ['dopamine', 'activity']:
                            status[key] = float(value)
                        elif key == 'idle_cycles':
                            status[key] = int(value)
                        elif key == 'is_sleeping':
                            status[key] = value == '1'
                return status
            except Exception:
                return None
        return None
    
    def _text_to_brain_input(self, text: str) -> List[float]:
        """Convert text to brain input vector (16 dimensions)"""
        words = text.lower().split()
        input_vec = []
        
        for word in words[:16]:
            h = hash(word) % 1000 / 1000.0
            input_vec.append(h)
        
        while len(input_vec) < 16:
            input_vec.append(0.0)
        
        return input_vec[:16]
    
    def _generate_microcontroller_commands(self):
        """Generate commands for microcontroller"""
        expr = self.biological.expressions
        
        cmd = {
            "type": "expression",
            "eyes": expr.current_eyes.value,
            "mouth": expr.current_mouth.value,
            "emotion": expr.current_emotion,
            "timestamp": time.time(),
        }
        self.microcontroller_commands.append(cmd)
    
    def _send_to_basal_ganglia(self, emotion: str, brain_input: List[float]):
        """Send data to basal ganglia"""
        # Send expression
        self.basal_ganglia.send_expression(emotion)
        
        # Send neural input
        self.basal_ganglia.send_input(brain_input)
    
    def _update_state(self):
        """Update complete state"""
        self.state.brain_activity = self.brain.global_activity
        self.state.brain_dopamine = self.brain.dopamine_level
        self.state.current_emotion = self.biological.emotions.current_emotion
        self.state.emotion_intensity = self.biological.emotions.emotion_intensity
        self.state.dopamine_level = self.biological.emotions.dopamine.get_level()
        self.state.is_bored = self.biological.emotions.is_bored()
        self.state.stm_count = len(self.memory.stm.memories)
        self.state.ltm_count = self.memory.ltm.get_memory_count()
        self.state.sleep_cycles = self.memory.sleep_cycle_count
        self.state.vocab_size = self.language.vocab.get_size()
        self.state.context_size = len(self.language.context.tokens)
        self.state.language_activity = self.language.activity_level
        self.state.thought_count = self.recursive.get_recursive_state().get("thought_count", 0)
        self.state.modifications = self.recursive.get_recursive_state().get("modifications", 0)
        self.state.uptime = time.time() - self.start_time