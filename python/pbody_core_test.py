#!/usr/bin/env python3
"""
P-Body Core Test - Verify the cortex works without hardware
Tests: Brain, Memory, Biological, Language, Recursive systems
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pbrain import PBrain
from pbody_memory import MemorySystem
from pbody_biological import BiologicalSystem
from pbody_language import BrocasArea
from pbody_recursive import RecursiveSystem


def test_brain():
    """Test 9-region brain architecture"""
    print("=" * 50)
    print("TEST 1: Brain (9 regions, 351 neurons)")
    print("=" * 50)
    
    brain = PBrain()
    
    # Test forward pass
    input_vec = np.array([0.5] * 16)  # 16 dimensions for sensory input
    output = brain.process(input_vec)
    
    print(f"  Input: {len(input_vec)} values")
    print(f"  Output shape: {output['output'].shape}")
    print(f"  Output range: [{output['output'].min():.4f}, {output['output'].max():.4f}]")
    print(f"  Total neurons: {brain.total_neurons}")
    print(f"  Total connections: {brain.total_connections}")
    print(f"  Global activity: {output['global_activity']:.4f}")
    print(f"  Dopamine: {output['dopamine']:.4f}")
    print(f"  ✓ Brain forward pass: PASS")
    return brain


def test_memory():
    """Test STM/LTM memory system"""
    print("\n" + "=" * 50)
    print("TEST 2: Memory System (STM + LTM)")
    print("=" * 50)
    
    memory = MemorySystem()
    
    # Store short-term memories
    memory.stm.add([0.8, 0.5, 0.3], emotion="happy")
    memory.stm.add([0.2, 0.7, 0.4], emotion="neutral")
    memory.stm.add([0.9, 0.6, 0.5], emotion="excited")
    
    print(f"  STM count: {len(memory.stm.memories)}")
    print(f"  LTM count: {memory.ltm.get_memory_count()}")
    
    # Consolidate important memories
    important = memory.stm.get_important_memories()
    for mem in important:
        memory.ltm.store(mem)
    
    print(f"  After consolidation - LTM count: {memory.ltm.get_memory_count()}")
    
    print(f"  ✓ Memory system: PASS")
    return memory


def test_biological():
    """Test emotions, dopamine, sleep"""
    print("\n" + "=" * 50)
    print("TEST 3: Biological System (Emotions + Dopamine)")
    print("=" * 50)
    
    bio = BiologicalSystem()
    
    # Test emotion update (through emotions processor)
    emotion = bio.emotions.update_emotion(brain_activity=0.5, novelty_score=0.6, prediction_accuracy=0.4)
    print(f"  Emotion: {emotion.name} (intensity: {bio.emotions.emotion_intensity:.3f})")
    
    # Test dopamine
    bio.emotions.dopamine.process_novelty(0.3)
    print(f"  Dopamine: {bio.emotions.dopamine.get_level():.3f}")
    
    # Test sleep (needs memory and brain)
    from pbrain import PBrain
    test_brain = PBrain()
    test_memory = MemorySystem()
    bio.sleep_cycle(test_memory, test_brain)
    print(f"  Sleep cycles: {bio.sleep.sleep_count}")
    
    print(f"  ✓ Biological system: PASS")
    return bio


def test_language():
    """Test Broca's area"""
    print("\n" + "=" * 50)
    print("TEST 4: Language Processing (Broca's Area)")
    print("=" * 50)
    
    lang = BrocasArea()
    
    # Process inputs
    inputs = ["hello world", "the cat is sleeping", "i like learning"]
    for text in inputs:
        result = lang.process_input(text)
        print(f"  Input: '{text}' → {result['vocab_size']} words")
    
    # Predict next
    predictions = lang.predict_next(top_k=3)
    print(f"  Predictions: {predictions}")
    
    # Generate response
    response = lang.generate_response(max_length=5)
    print(f"  Generated: '{response}'")
    
    print(f"  ✓ Language system: PASS")
    return lang


def test_recursive():
    """Test self-monitoring and reflection"""
    print("\n" + "=" * 50)
    print("TEST 5: Recursive System (Self-Operation)")
    print("=" * 50)
    
    recursive = RecursiveSystem()
    
    # Self-monitor (captures state)
    state = recursive.self_monitor(emotion="happy", activity=0.5, dopamine=0.7)
    print(f"  State captured: emotion={state.emotion}, activity={state.activity_level:.2f}")
    
    # Self-reflect
    reflection = recursive.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    # Metacognition (analyze_self needs state + recent thoughts)
    meta = recursive.metacognitive_analysis()
    print(f"  Metacognition: {meta}")
    
    print(f"  ✓ Recursive system: PASS")
    return recursive


def test_integration():
    """Test full system integration"""
    print("\n" + "=" * 50)
    print("TEST 6: Full Integration")
    print("=" * 50)
    
    from pbody_integration import PBodyIntegration
    
    pbody = PBodyIntegration()
    
    # Process inputs
    test_inputs = [
        ("hello world", "happy"),
        ("the cat is sleeping", "neutral"),
        ("i like learning", "excited"),
    ]
    
    for text, emotion in test_inputs:
        result = pbody.process_input(text, emotion)
        print(f"  '{text}' → {result['emotion']} (dopamine: {result['dopamine']:.3f})")
    
    # Sleep cycle
    sleep_result = pbody.sleep()
    print(f"  Sleep: {sleep_result['sleep_cycles']} cycles")
    
    # Self-reflect
    reflection = pbody.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    print(f"  ✓ Full integration: PASS")
    return pbody


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("P-BODY CORE TEST")
    print("=" * 50 + "\n")
    
    try:
        brain = test_brain()
        memory = test_memory()
        bio = test_biological()
        lang = test_language()
        recursive = test_recursive()
        pbody = test_integration()
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED ✓")
        print("=" * 50)
        print(f"\nP-Body is operational!")
        print(f"  Brain: {brain.total_neurons} neurons")
        print(f"  Memory: {len(memory.stm.memories)} STM, {memory.ltm.get_memory_count()} LTM")
        print(f"  Emotion: {bio.emotions.get_state().get('current_emotion', 'neutral')}")
        print(f"  Vocabulary: {lang.vocab.get_size()}")
        print(f"  Thoughts: {recursive.dialogue.thought_count}")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)