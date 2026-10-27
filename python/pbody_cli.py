#!/usr/bin/env python3
"""
P-Body CLI - Command Line Interface
Communicate with P-Body via terminal
Includes Basal Ganglia communication
"""

import sys
import time
import argparse
import json
from typing import Optional

from pbody_integration import PBodyIntegration


class PBodyCLI:
    """Interactive CLI for P-Body"""
    
    def __init__(self, verbose: bool = False, serial_port: Optional[str] = None):
        self.pbody = PBodyIntegration(name="P-Body", serial_port=serial_port)
        self.verbose = verbose
        self.running = True
        self.history = []
    
    def run(self):
        """Main CLI loop"""
        print("=" * 60)
        print("  P-Body CLI - Command Line Interface")
        print("=" * 60)
        print()
        print("Commands:")
        print("  <text>          - Talk to P-Body")
        print("  /state          - Show current state")
        print("  /reflect        - Self-reflection")
        print("  /sleep          - Run sleep cycle")
        print("  /response       - Get P-Body's response")
        print("  /history        - Show input history")
        print("  /basal          - Show basal ganglia status")
        print("  /commands       - List commands")
        print("  /verbose        - Toggle verbose mode")
        print("  /quit           - Exit")
        print()
        print("Type your message and press Enter to talk to P-Body.")
        print()
        
        while self.running:
            try:
                user_input = input("You> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                else:
                    self._process_input(user_input)
            
            except KeyboardInterrupt:
                print("\n\n[P-Body] Goodbye!")
                break
            except EOFError:
                print("\n\n[P-Body] Goodbye!")
                break
    
    def _handle_command(self, command: str):
        """Handle CLI commands"""
        cmd = command.lower().strip()
        
        if cmd == "/quit" or cmd == "/exit":
            self.running = False
            self.pbody.basal_ganglia.disconnect()
            print("[P-Body] Goodbye!")
        
        elif cmd == "/state":
            self._show_state()
        
        elif cmd == "/reflect":
            self._show_reflection()
        
        elif cmd == "/sleep":
            self._run_sleep()
        
        elif cmd == "/response":
            self._show_response()
        
        elif cmd == "/history":
            self._show_history()
        
        elif cmd == "/basal":
            self._show_basal_status()
        
        elif cmd == "/commands":
            self._show_commands()
        
        elif cmd == "/verbose":
            self.verbose = not self.verbose
            print(f"[P-Body] Verbose mode: {'ON' if self.verbose else 'OFF'}")
        
        else:
            print(f"[P-Body] Unknown command: {cmd}")
            print("Type /commands for available commands")
    
    def _process_input(self, text: str):
        """Process user input through P-Body"""
        # Record input
        self.history.append({
            "input": text,
            "timestamp": time.time()
        })
        
        # Process through P-Body
        result = self.pbody.process_input(text)
        
        # Show result
        emotion = result.get("emotion", "neutral")
        expression = result.get("expression", {})
        brain_activity = result.get("brain_activity", 0.0)
        dopamine = result.get("dopamine", 0.5)
        
        # Show expression
        eyes = expression.get("eyes", "open")
        mouth = expression.get("mouth", "normal")
        print(f"\n[P-Body] [{eyes} eyes + {mouth} mouth] Emotion: {emotion}")
        
        # Get response
        response = self.pbody.get_response()
        if response:
            print(f"P-Body> {response}")
        else:
            print(f"P-Body> ...")
        
        # Verbose info
        if self.verbose:
            print(f"  [Brain Activity: {brain_activity:.4f}]")
            print(f"  [Dopamine: {dopamine:.4f}]")
            print(f"  [Vocab: {self.pbody.state.vocab_size}]")
            print(f"  [STM: {self.pbody.state.stm_count}]")
            print(f"  [LTM: {self.pbody.state.ltm_count}]")
            print(f"  [Basal Ganglia: {'Connected' if self.pbody.basal_ganglia.connected else 'Queued'}]")
        
        print()
    
    def _show_state(self):
        """Show current P-Body state"""
        state = self.pbody.get_state()
        
        print("\n--- P-Body State ---")
        print(f"Emotion: {state.current_emotion}")
        print(f"Emotion Intensity: {state.emotion_intensity:.4f}")
        print(f"Dopamine: {state.dopamine_level:.4f}")
        print(f"Brain Activity: {state.brain_activity:.4f}")
        print(f"Is Bored: {state.is_bored}")
        print(f"STM Memories: {state.stm_count}")
        print(f"LTM Memories: {state.ltm_count}")
        print(f"Sleep Cycles: {state.sleep_cycles}")
        print(f"Vocabulary: {state.vocab_size}")
        print(f"Context Size: {state.context_size}")
        print(f"Language Activity: {state.language_activity:.4f}")
        print(f"Thoughts: {state.thought_count}")
        print(f"Self-Modifications: {state.modifications}")
        print(f"Total Inputs: {state.total_inputs}")
        print(f"Uptime: {state.uptime:.2f}s")
        print(f"Basal Ganglia: {'Connected' if self.pbody.basal_ganglia.connected else 'Queued'}")
        print()
    
    def _show_basal_status(self):
        """Show basal ganglia status"""
        bg = self.pbody.basal_ganglia
        
        print("\n--- Basal Ganglia Status ---")
        print(f"Connected: {bg.connected}")
        print(f"Port: {bg.port or 'Not set'}")
        print(f"Baud: {bg.baud}")
        print(f"Queued Commands: {len(bg.command_queue)}")
        
        if bg.command_queue:
            print("\nRecent Commands:")
            for cmd in bg.command_queue[-5:]:
                print(f"  {cmd}")
        
        # Try to get live status
        live_status = self.pbody.get_basal_ganglia_status()
        if live_status:
            print(f"\nLive Status:")
            for key, value in live_status.items():
                print(f"  {key}: {value}")
        print()
    
    def _show_reflection(self):
        """Show self-reflection"""
        reflection = self.pbody.self_reflect()
        
        print("\n--- Self-Reflection ---")
        print(f"Reflection: {reflection['reflection']}")
        print(f"\nRecent Thoughts:")
        for i, thought in enumerate(reflection['thoughts'], 1):
            print(f"  {i}. {thought}")
        
        if reflection.get('analysis'):
            print(f"\nAnalysis: {reflection['analysis']}")
        print()
    
    def _run_sleep(self):
        """Run sleep cycle"""
        result = self.pbody.sleep()
        
        print("\n--- Sleep Cycle Complete ---")
        print(f"Sleep Cycles: {result['sleep_cycles']}")
        print(f"Memories Consolidated: {result['memories_consolidated']}")
        print(f"Memories Pruned: {result['memories_pruned']}")
        print(f"Expression: {result['expression']}")
        print()
    
    def _show_response(self):
        """Show P-Body's generated response"""
        response = self.pbody.get_response()
        
        if response:
            print(f"\nP-Body> {response}")
        else:
            print("\nP-Body> (no response - context is empty)")
        print()
    
    def _show_history(self):
        """Show input history"""
        if not self.history:
            print("\n[No history yet]")
            return
        
        print("\n--- Input History ---")
        for i, entry in enumerate(self.history[-10:], 1):
            print(f"  {i}. {entry['input']}")
        print()
    
    def _show_commands(self):
        """Show available commands"""
        print("\n--- Available Commands ---")
        print("  <text>          - Talk to P-Body")
        print("  /state          - Show current state")
        print("  /reflect        - Self-reflection")
        print("  /sleep          - Run sleep cycle")
        print("  /response       - Get P-Body's response")
        print("  /history        - Show input history")
        print("  /basal          - Show basal ganglia status")
        print("  /commands       - List commands")
        print("  /verbose        - Toggle verbose mode")
        print("  /quit           - Exit")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="P-Body CLI")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("-p", "--port", type=str,
                       help="Serial port for basal ganglia (e.g., /dev/ttyUSB0)")
    
    args = parser.parse_args()
    
    cli = PBodyCLI(verbose=args.verbose, serial_port=args.port)
    cli.run()


if __name__ == "__main__":
    main()