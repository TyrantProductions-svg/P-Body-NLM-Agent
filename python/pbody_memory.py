"""
P-Body Memory Architecture
Phase 2: Short-term memory, long-term memory, associative links, emotion tagging
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import time


@dataclass
class Memory:
    """A single memory unit"""
    content: List[float]  # The actual memory data (activations/patterns)
    importance: float = 0.5  # How important this memory is (0-1)
    emotion_tag: str = "neutral"  # Emotional valence
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0  # How often accessed (affects importance)
    associative_links: List[int] = field(default_factory=list)  # IDs of related memories
    
    def reinforce(self):
        """Increase importance when accessed"""
        self.access_count += 1
        self.importance = min(1.0, self.importance + 0.1)
    
    def decay(self, rate: float = 0.05):
        """Decrease importance over time (forgetting)"""
        self.importance = max(0.0, self.importance - rate)


class ShortTermMemory:
    """Working memory buffer - holds recent/active memories"""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.memories: List[Memory] = []
        self.current_focus: Optional[Memory] = None
    
    def add(self, content: List[float], emotion: str = "neutral") -> Memory:
        """Add new memory to short-term storage"""
        memory = Memory(content=content, emotion_tag=emotion)
        
        if len(self.memories) >= self.capacity:
            # Remove least important memory
            self.memories.sort(key=lambda m: m.importance)
            removed = self.memories.pop(0)
            print(f"  [STM] Forgotten: {removed.content[:3]}... (importance: {removed.importance:.2f})")
        
        self.memories.append(memory)
        self.current_focus = memory
        print(f"  [STM] Stored: {content[:3]}... (emotion: {emotion})")
        return memory
    
    def get_recent(self, count: int = 3) -> List[Memory]:
        """Get most recent memories"""
        return self.memories[-count:]
    
    def get_focus(self) -> Optional[Memory]:
        """Get currently focused memory"""
        return self.current_focus
    
    def decay_all(self, rate: float = 0.05):
        """Decay all memories (forgetting mechanism)"""
        for memory in self.memories:
            memory.decay(rate)
    
    def get_important_memories(self) -> List[Memory]:
        """Get memories above importance threshold for consolidation"""
        threshold = 0.7
        return [m for m in self.memories if m.importance >= threshold]
    
    def clear(self):
        """Clear all short-term memories (after sleep consolidation)"""
        self.memories.clear()
        self.current_focus = None


class LongTermMemory:
    """Permanent memory storage - consolidated memories"""
    
    def __init__(self):
        self.memories: Dict[int, Memory] = {}  # ID -> Memory
        self.next_id: int = 0
        self.associative_index: Dict[str, List[int]] = {}  # Emotion -> Memory IDs
    
    def store(self, memory: Memory) -> int:
        """Consolidate memory from short-term to long-term"""
        memory_id = self.next_id
        self.next_id += 1
        
        self.memories[memory_id] = memory
        
        # Index by emotion for associative retrieval
        emotion = memory.emotion_tag
        if emotion not in self.associative_index:
            self.associative_index[emotion] = []
        self.associative_index[emotion].append(memory_id)
        
        print(f"  [LTM] Consolidated: ID {memory_id} (emotion: {emotion}, importance: {memory.importance:.2f})")
        return memory_id
    
    def retrieve(self, memory_id: int) -> Optional[Memory]:
        """Retrieve specific memory by ID"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.reinforce()
            return memory
        return None
    
    def retrieve_by_emotion(self, emotion: str, count: int = 5) -> List[Memory]:
        """Retrieve memories with specific emotional tag"""
        if emotion in self.associative_index:
            ids = self.associative_index[emotion][-count:]
            return [self.memories[id] for id in ids if id in self.memories]
        return []
    
    def find_similar(self, content: List[float], threshold: float = 0.8) -> List[Tuple[int, Memory]]:
        """Find memories similar to input pattern"""
        similar = []
        
        for memory_id, memory in self.memories.items():
            # Calculate similarity (cosine similarity simplified)
            if len(memory.content) == len(content):
                dot_product = sum(a * b for a, b in zip(memory.content, content))
                magnitude = (sum(a * a for a in content) ** 0.5) * (sum(b * b for b in memory.content) ** 0.5)
                
                if magnitude > 0:
                    similarity = dot_product / magnitude
                    if similarity >= threshold:
                        similar.append((memory_id, memory))
                        print(f"  [LTM] Found similar: ID {memory_id} (similarity: {similarity:.2f})")
        
        return similar
    
    def get_all_ids(self) -> List[int]:
        """Get all memory IDs"""
        return list(self.memories.keys())
    
    def get_memory_count(self) -> int:
        """Get total number of long-term memories"""
        return len(self.memories)


class MemorySystem:
    """Complete memory system with STM, LTM, and associative links"""
    
    def __init__(self, stm_capacity: int = 10):
        self.stm = ShortTermMemory(capacity=stm_capacity)
        self.ltm = LongTermMemory()
        self.sleep_cycle_count: int = 0
    
    def experience(self, content: List[float], emotion: str = "neutral"):
        """Process new experience"""
        print(f"\n[Memory] New experience: {content[:3]}... (emotion: {emotion})")
        
        # Add to short-term memory
        memory = self.stm.add(content, emotion)
        
        # Check for similar long-term memories (associative linking)
        similar = self.ltm.find_similar(content, threshold=0.7)
        
        if similar:
            print(f"  [Memory] Found {len(similar)} similar memories in LTM")
            # Create associative links
            for mem_id, _ in similar:
                memory.associative_links.append(mem_id)
        else:
            print(f"  [Memory] No similar memories found (novel experience)")
    
    def recall(self, cue: List[float]) -> List[Memory]:
        """Recall memories based on cue"""
        print(f"\n[Memory] Recalling with cue: {cue[:3]}...")
        
        # Search long-term memory
        similar = self.ltm.find_similar(cue, threshold=0.6)
        
        if similar:
            memories = [mem for _, mem in similar]
            print(f"  [Memory] Recalled {len(memories)} memories")
            return memories
        else:
            print(f"  [Memory] No memories recalled")
            return []
    
    def sleep_consolidate(self):
        """Sleep cycle: consolidate important memories, prune unimportant ones"""
        print(f"\n{'='*50}")
        print(f"[Sleep] Starting sleep cycle #{self.sleep_cycle_count + 1}")
        print(f"{'='*50}")
        
        # Get important memories from STM
        important = self.stm.get_important_memories()
        consolidated_count = len(important)
        
        print(f"\n[Sleep] Consolidating {consolidated_count} important memories...")
        for memory in important:
            self.ltm.store(memory)
        
        # Decay remaining STM memories
        print(f"\n[Sleep] Decaying remaining STM memories...")
        self.stm.decay_all(rate=0.2)
        
        # Count memories before clearing
        stm_count = len(self.stm.memories)
        
        # Clear STM
        print(f"\n[Sleep] Clearing short-term memory...")
        self.stm.clear()
        
        self.sleep_cycle_count += 1
        print(f"\n[Sleep] Sleep cycle complete. LTM now has {self.ltm.get_memory_count()} memories")
        print(f"{'='*50}\n")
        
        return {
            "consolidated": consolidated_count,
            "pruned": stm_count,
            "ltm_count": self.ltm.get_memory_count(),
        }
    
    def get_state(self) -> dict:
        """Get current memory system state"""
        return {
            "stm_count": len(self.stm.memories),
            "ltm_count": self.ltm.get_memory_count(),
            "sleep_cycles": self.sleep_cycle_count,
            "stm_memories": [
                {
                    "content": m.content[:3],
                    "importance": m.importance,
                    "emotion": m.emotion_tag
                }
                for m in self.stm.memories
            ],
            "ltm_emotions": {
                emotion: len(ids) 
                for emotion, ids in self.ltm.associative_index.items()
            }
        }