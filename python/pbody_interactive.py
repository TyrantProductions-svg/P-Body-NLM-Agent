#!/usr/bin/env python3
"""
P-Body Interactive Chat
Test P-Body's learning and responses on your computer before deploying to Arduino.
"""

import sys
import os
import contextlib
import io
sys.path.insert(0, os.path.dirname(__file__))

from pbody_integration import PBodyIntegration


@contextlib.contextmanager
def suppress_stdout():
    """Suppress all print output from internal systems"""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def print_separator(char="=", length=60):
    print(char * length)


def print_state(pbody):
    """Print P-Body's current internal state"""
    state = pbody.get_state()
    print()
    print_separator("-", 50)
    print(f"  Emotion:       {state.current_emotion} ({state.emotion_intensity:.2f})")
    print(f"  Dopamine:      {state.dopamine_level:.3f}")
    print(f"  Brain Activity:{state.brain_activity:.3f}")
    print(f"  STM Memories:  {state.stm_count}")
    print(f"  LTM Memories:  {state.ltm_count}")
    print(f"  Vocabulary:    {state.vocab_size}")
    print(f"  Total Inputs:  {state.total_inputs}")
    print(f"  Sleep Cycles:  {state.sleep_cycles}")
    print_separator("-", 50)


def print_help():
    print()
    print("Commands:")
    print("  <text>        - Talk to P-Body")
    print("  /state        - Show internal state")
    print("  /reflect      - Show self-reflection")
    print("  /sleep        - Run sleep cycle")
    print("  /memory       - Show memories")
    print("  /vocab        - Show vocabulary")
    print("  /help         - Show this help")
    print("  /quit         - Exit")
    print()


def main():
    print_separator()
    print("  P-BODY INTERACTIVE TEST")
    print_separator()
    print()
    print("Type to interact. P-Body will learn and respond.")
    print("Use /help for commands, /quit to exit.")
    print()

    pbody = PBodyIntegration()
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nBye!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input[1:].lower()

            if cmd == "quit" or cmd == "exit":
                print("Bye!")
                break
            elif cmd == "help":
                print_help()
            elif cmd == "state":
                print_state(pbody)
            elif cmd == "reflect":
                reflection = pbody.self_reflect()
                print()
                print("  Self-Reflection:")
                print(f"    {reflection['reflection']}")
                print(f"    Insights: {reflection['analysis'].get('insight', 'none')}")
            elif cmd == "sleep":
                result = pbody.sleep()
                print(f"\n  Slept. {result['memories_consolidated']} consolidated, {result['memories_pruned']} pruned.")
            elif cmd == "memory":
                print()
                print(f"  STM: {len(pbody.memory.stm.memories)} memories")
                for i, mem in enumerate(pbody.memory.stm.memories[-5:]):
                    print(f"    [{i}] {mem.content[:3]}... (emotion: {mem.emotion_tag})")
                print(f"  LTM: {pbody.memory.ltm.get_memory_count()} memories")
            elif cmd == "vocab":
                words = list(pbody.language.vocab.word_to_id.keys())[:20]
                print(f"\n  Vocabulary ({pbody.language.vocab.get_size()} words): {', '.join(words)}")
            else:
                print(f"  Unknown command: {cmd}")
            continue

        with suppress_stdout():
            result = pbody.process_input(user_input)
        response = pbody.get_response()

        print(f"  P-Body: {response}")
        print(f"  (emotion: {result['emotion']}, dopamine: {result['dopamine']:.3f})")
        print()


if __name__ == "__main__":
    main()