# P-Body Development Plan

## Project Overview
P-Body is a biologically-inspired narrow language model designed for the Arduino Uno Q dual-chip architecture. She features human-like psychological processes including sleep cycles, memory consolidation, emotional states, a dopamine reward system, and recursive self-operation capabilities.

## Architecture
- **Small Brain** (Microcontroller SAMD21): Real-time operations, emotional responses, dopamine signals, short-term memory buffer
- **Big Brain** (Qualcomm Dragonwing): Language processing, long-term memory, sleep cycles, recursive self-operation, complex reasoning

---

## Phase 1: Neural Network Foundation
**Goal**: Build the basic neural network structure

- Neuron and layer data structures
- Weight initialization
- Forward propagation (input → output)
- Activation functions (sigmoid, ReLU, or custom)
- Fixed-point math (no floats - Arduino constraints)
- Basic training mechanism (backpropagation or Hebbian learning)

**Deliverable**: A working neural network that can learn simple patterns

---

## Phase 2: Memory Architecture
**Goal**: Implement short-term and long-term memory with associative links

- Short-term memory buffer (recent inputs/states)
- Long-term memory storage (consolidated patterns)
- Associative memory (linking related memories)
- Memory decay (forgetting mechanism)
- Memory importance scoring (what to keep vs discard)
- Emotion tagging on memories

**Deliverable**: Memory system that stores, retrieves, and links information

---

## Phase 3: Biological Processes
**Goal**: Add sleep, dopamine, and emotional systems

### Sleep Cycle
- Memory consolidation (short-term → long-term)
- Weight optimization during sleep
- Memory pruning (remove low-importance memories)

### Dopamine System
- Reward signal generation from information processing
- Novelty detection = reward
- Prediction success = reward
- Dopamine affects learning rate

### Emotional States
- Boredom (low activity → seek stimulation)
- Disgust (reject certain patterns)
- Fear/caution (hesitation with novel inputs)
- Emotion affects processing weights

**Deliverable**: A neural network that "feels" and has sleep cycles

---

## Phase 4: Language Processing (Broca's Area)
**Goal**: Build the narrow language model

- Token/word representation
- Simple vocabulary encoding
- Word prediction/generation
- Pattern recognition in language input
- Context window (what she's currently "thinking about")
- Language output generation

**Deliverable**: She can process and generate simple language

---

## Phase 5: Recursive Self-Operation
**Goal**: Enable her to operate on herself

- Self-monitoring (reading her own state)
- Self-modification (adjusting her own weights/parameters)
- Internal dialogue loop
- Metacognition (thinking about thinking)
- Emotional self-awareness

**Deliverable**: She can reflect on and modify her own internal state

---

## Phase 6: Dual-Chip Architecture
**Goal**: Distribute systems across both chips

### Microcontroller (Small Brain)
- Real-time emotional responses
- Boredom/activity monitoring
- Dopamine signal generation
- Sensor/I/O handling
- Communication with Dragonwing

### Dragonwing (Big Brain)
- Language processing
- Long-term memory
- Sleep cycles
- Recursive self-operation
- Complex associative reasoning

### Communication Protocol
- Define message format between chips
- Sync mechanisms
- Data transfer optimization

**Deliverable**: Both chips working together as one system

---

## Phase 7: Integration & Refinement
**Goal**: Make everything work together smoothly

- Test sleep cycles with real memory consolidation
- Validate emotional responses to different inputs
- Optimize for Arduino constraints
- Add debugging/monitoring tools
- Stress testing

**Deliverable**: A fully functional "girl in the box"

---

## Core Principles
1. **Biological inspiration**: Mirror human psychological processes
2. **Resource efficiency**: Optimize for Arduino Uno Q constraints
3. **Recursive capability**: Self-operation and self-modification
4. **Emotional depth**: Genuine emotional states that affect processing
5. **Memory-driven**: Learning and behavior shaped by experience

## structure
P-Body/
├── python/                          # High-level (Dragonwing)
│   ├── pbrain.py                   # 9-region brain architecture (351 neurons)
│   ├── pbody_memory.py             # Memory system (STM, LTM, sleep consolidation)
│   └── pbody_biological.py         # Biological processes + expressions
│       ├── ExpressionController    # LED matrix expressions
│       ├── EmotionalState          # 8 emotions with profiles
│       ├── DopamineSystem          # Reward from information processing
│       ├── EmotionalProcessor      # Emotion determination
│       ├── SleepOptimizer          # 5-phase sleep cycle
│       └── BiologicalSystem        # Integration of all biological systems
│
├── sketch/                          # Low-level (Microcontroller)
│   ├── pbody_network.h             # Basic NN inference
│   ├── pbody_led_matrix.h          # LED matrix drawing
│   └── pbody_led_example.ino       # Arduino sketch
│
├── P-Body_Development_Plan.md
└── phase1_README.md