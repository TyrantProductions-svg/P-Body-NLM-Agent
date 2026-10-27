#!/usr/bin/env python3
"""
P-Body Complete Test Suite
Tests: Brain, Memory, Biological, Language, Recursive, Integration, Edge Cases
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


# ============================================================
# CORE SYSTEM TESTS
# ============================================================

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


# ============================================================
# RECURSIVE SYSTEM EDGE CASE TESTS
# ============================================================

def test_no_systems():
    """Test: RecursiveSystem with NO connected systems"""
    print("\n" + "=" * 50)
    print("EDGE 1: No connected systems (all None)")
    print("=" * 50)
    
    recursive = RecursiveSystem()  # No brain, memory, biological, language
    
    # Should not crash
    state = recursive.self_monitor()
    print(f"  State: emotion={state.emotion}, activity={state.activity_level}")
    
    # Should not crash
    reflection = recursive.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    # Should not crash
    meta = recursive.metacognitive_analysis()
    print(f"  Meta: {meta}")
    
    # Should not crash
    thoughts = recursive.internal_dialogue_loop(2)
    print(f"  Thoughts: {thoughts}")
    
    print("  ✓ PASS: No crashes with empty systems")


def test_partial_systems():
    """Test: Only some systems connected"""
    print("\n" + "=" * 50)
    print("EDGE 2: Partial systems (brain + memory only)")
    print("=" * 50)
    
    brain = PBrain()
    memory = MemorySystem()
    
    recursive = RecursiveSystem(brain=brain, memory=memory)
    
    # Should not crash
    state = recursive.self_monitor()
    print(f"  State: emotion={state.emotion}, memory_count={state.memory_count}")
    
    # Should not crash
    reflection = recursive.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    print("  ✓ PASS: No crashes with partial systems")


def test_self_modify_edge_cases():
    """Test: Self-modification edge cases"""
    print("\n" + "=" * 50)
    print("EDGE 3: Self-modification edge cases")
    print("=" * 50)
    
    recursive = RecursiveSystem()
    
    # Invalid parameter
    result = recursive.self_modify("invalid_param", 0.5)
    print(f"  Invalid param: {result}")
    assert result == False
    
    # Out of range
    result = recursive.self_modify("learning_rate", 999.0)
    print(f"  Out of range: {result}")
    assert result == False
    
    # Valid modification
    result = recursive.self_modify("learning_rate", 0.1, reason="testing")
    print(f"  Valid mod: {result}")
    assert result == True
    
    print("  ✓ PASS: Self-modification handles edge cases")


def test_rapid_operations():
    """Test: Many operations in quick succession"""
    print("\n" + "=" * 50)
    print("EDGE 4: Rapid operations (stress test)")
    print("=" * 50)
    
    recursive = RecursiveSystem()
    
    # 20 rapid operations
    for i in range(20):
        recursive.self_monitor(emotion="happy", activity=i * 0.05)
    
    print(f"  Operations: {recursive.operation_count}")
    print(f"  History: {len(recursive.monitor.state_history)}")
    
    # Reflect after many operations
    reflection = recursive.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    # Metacognitive analysis
    meta = recursive.metacognitive_analysis()
    print(f"  Analysis keys: {list(meta.keys())}")
    
    print("  ✓ PASS: Rapid operations handled")


def test_empty_history_operations():
    """Test: Operations on empty history"""
    print("\n" + "=" * 50)
    print("EDGE 5: Empty history operations")
    print("=" * 50)
    
    recursive = RecursiveSystem()
    
    # Reflect before any monitoring
    reflection = recursive.self_reflect()
    print(f"  Reflection (empty): '{reflection}'")
    
    # Meta before any monitoring
    meta = recursive.metacognitive_analysis()
    print(f"  Meta (empty): {meta}")
    assert "analysis" in meta
    assert "insight" in meta
    
    # Internal dialogue before monitoring
    thoughts = recursive.internal_dialogue_loop(3)
    print(f"  Thoughts (empty): {thoughts}")
    assert len(thoughts) == 3
    
    print("  ✓ PASS: Empty history handled")


def test_full_systems_edge():
    """Test: All systems connected, edge cases"""
    print("\n" + "=" * 50)
    print("EDGE 6: Full systems edge cases")
    print("=" * 50)
    
    brain = PBrain()
    memory = MemorySystem()
    biological = BiologicalSystem()
    language = BrocasArea()
    
    recursive = RecursiveSystem(
        brain=brain,
        memory=memory,
        biological=biological,
        language=language
    )
    
    # Monitor (pulls from all systems)
    state = recursive.self_monitor()
    print(f"  State: emotion={state.emotion}, vocab={state.vocab_size}")
    print(f"  Activity: {state.activity_level:.4f}")
    print(f"  Dopamine: {state.dopamine_level:.4f}")
    
    # Modify learning rate
    result = recursive.self_modify("learning_rate", 0.05, reason="testing")
    print(f"  Modified learning_rate: {result}")
    
    # Reflect
    reflection = recursive.self_reflect()
    print(f"  Reflection: '{reflection}'")
    
    # Meta
    meta = recursive.metacognitive_analysis()
    print(f"  Meta insight: {meta.get('insight', 'none')}")
    
    print("  ✓ PASS: Full systems edge cases handled")


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_core_tests():
    """Run core system tests"""
    print("\n" + "=" * 50)
    print("P-BODY CORE TESTS")
    print("=" * 50 + "\n")
    
    brain = test_brain()
    memory = test_memory()
    bio = test_biological()
    lang = test_language()
    recursive = test_recursive()
    pbody = test_integration()
    
    print("\n" + "=" * 50)
    print("CORE TESTS PASSED ✓")
    print("=" * 50)
    print(f"\nP-Body is operational!")
    print(f"  Brain: {brain.total_neurons} neurons")
    print(f"  Memory: {len(memory.stm.memories)} STM, {memory.ltm.get_memory_count()} LTM")
    print(f"  Emotion: {bio.emotions.get_state().get('current_emotion', 'neutral')}")
    print(f"  Vocabulary: {lang.vocab.get_size()}")
    print(f"  Thoughts: {recursive.dialogue.thought_count}")
    
    return brain, memory, bio, lang, recursive, pbody


def run_edge_tests():
    """Run recursive system edge case tests"""
    print("\n" + "=" * 50)
    print("P-BODY RECURSIVE - EDGE CASE TESTS")
    print("=" * 50 + "\n")
    
    test_no_systems()
    test_partial_systems()
    test_self_modify_edge_cases()
    test_rapid_operations()
    test_empty_history_operations()
    test_full_systems_edge()
    
    print("\n" + "=" * 50)
    print("EDGE CASE TESTS PASSED ✓")
    print("=" * 50)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("P-BODY COMPLETE TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        # Run core tests
        run_core_tests()
        
        # Run edge case tests
        run_edge_tests()
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED ✓")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)