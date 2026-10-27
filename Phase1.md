# Phase 1: Neural Network Foundation

## Overview
This phase builds the basic neural network structure with fixed-point math support for Arduino constraints.

## Files Created

### 1. `pbody_neural_network.py`
- **Purpose**: Python implementation for testing and Dragonwing development
- **Features**:
  - Fixed-point math class (Q15.16 format)
  - Neuron with weights, bias, activation
  - Layer with multiple neurons
  - Complete neural network with forward propagation
  - Simple training mechanism
  - Test with XOR problem

### 2. `pbody_network.h`
- **Purpose**: C++ header for Arduino microcontroller
- **Features**:
  - Fixed-point arithmetic functions
  - Neuron, Layer, and Network structures
  - Memory-efficient design for microcontroller constraints
  - Sigmoid and ReLU activations

### 3. `pbody_example.ino`
- **Purpose**: Arduino sketch demonstrating the network
- **Features**:
  - Network initialization
  - Test cases with sample inputs
  - Serial output for debugging

## How to Test

### On Your Computer (Python):
```bash
cd python
python pbody_neural_network.py
```

This will:
1. Create a neural network (2 inputs → 4 hidden → 1 output)
2. Train it on the XOR problem
3. Show results after training

### On Arduino Microcontroller:
1. Open `pbody_example.ino` in Arduino IDE
2. Select your board (Arduino Uno Q microcontroller)
3. Upload to board
4. Open Serial Monitor (115200 baud)
5. See network test results

## Next Steps (Phase 2)
- Memory architecture (short-term/long-term)
- Associative memory links
- Emotion tagging on memories
- Memory decay mechanism

## Architecture Notes

### Fixed-Point Math (Q15.16)
- 15 bits for integer part
- 16 bits for fractional part
- Range: -32768 to 32767.99998
- Precision: ~0.000015

### Why Fixed-Point?
- Microcontrollers struggle with floating-point
- Fixed-point is faster and more predictable
- Uses less memory
- Essential for real-time operation

### Network Structure
```
Input Layer → Hidden Layer(s) → Output Layer
   [2]           [4]              [1]
```

Each connection has a weight, each neuron has a bias.