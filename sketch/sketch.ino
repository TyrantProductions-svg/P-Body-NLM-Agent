/*
 * P-Body Basal Ganglia / Master Gland
 * 
 * This is the central coordinator for P-Body's microcontroller side.
 * Acts as the basal ganglia - handles automatic reflexes, real-time operations,
 * and communication between the microcontroller and Dragonwing.
 * 
 * Functions:
 * - Initialize all subsystems
 * - Manage serial communication with Dragonwing
 * - Execute reflexive behaviors (fear, surprise, etc.)
 * - Monitor activity levels (boredom detection)
 * - Generate dopamine-like signals
 * - Coordinate LED expressions
 */

#include "pbody_led_matrix.h"
#include "pbody_network.h"

// ============================================
// Configuration
// ============================================
#define SERIAL_BAUD 115200
#define ACTIVITY_CHECK_INTERVAL 5000  // Check activity every 5 seconds
#define DOPAMINE_DECAY_RATE 0.01      // Dopamine decay per cycle
#define BOREDOM_THRESHOLD 10          // Cycles without input = bored

// ============================================
// State Variables
// ============================================
PBodyNetwork brain;
uint32_t last_activity_time = 0;
uint32_t last_check_time = 0;
uint32_t idle_cycles = 0;
float dopamine_level = 0.5;
bool is_sleeping = false;
bool is_initialized = false;

// ============================================
// Basal Ganglia Functions
// ============================================

/*
 * Initialize all subsystems
 * This is the "waking up" sequence
 */
void basal_ganglia_init() {
    Serial.begin(SERIAL_BAUD);
    delay(1000);
    
    Serial.println("[Basal Ganglia] Initializing...");
    
    // Initialize LED matrix
    matrix_clear();
    show_neutral();
    
    // Initialize neural network (simple 3-layer)
    int sizes[] = {16, 8, 4};
    brain.init(sizes, 3);
    brain.dopamine_level = to_fixed(0.5);
    
    // Set initial state
    last_activity_time = millis();
    last_check_time = millis();
    idle_cycles = 0;
    dopamine_level = 0.5;
    is_sleeping = false;
    is_initialized = true;
    
    Serial.println("[Basal Ganglia] Ready");
    Serial.println("[Basal Ganglia] Waiting for input...");
}

/*
 * Check for incoming commands from Dragonwing
 * Returns true if command was processed
 */
bool check_dragonwing_input() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command.length() > 0) {
            process_command(command);
            last_activity_time = millis();
            idle_cycles = 0;
            dopamine_level = min(1.0, dopamine_level + 0.1);
            return true;
        }
    }
    return false;
}

/*
 * Process commands from Dragonwing
 */
void process_command(String command) {
    Serial.print("[Basal Ganglia] Received: ");
    Serial.println(command);
    
    if (command.startsWith("expression:")) {
        String expr = command.substring(11);
        expr.trim();
        set_expression_by_name(expr);
    }
    else if (command == "sleep") {
        enter_sleep_mode();
    }
    else if (command == "wake") {
        exit_sleep_mode();
    }
    else if (command == "status") {
        send_status();
    }
    else if (command.startsWith("input:")) {
        String input = command.substring(6);
        process_neural_input(input);
    }
}

/*
 * Set expression by name
 */
void set_expression_by_name(String name) {
    if (name == "happy") show_happy();
    else if (name == "teasing") show_teasing();
    else if (name == "sleeping") show_sleeping();
    else if (name == "fear") show_fear();
    else if (name == "disgust") show_disgust();
    else if (name == "neutral") show_neutral();
    else if (name == "caution") show_caution();
    else if (name == "bored") show_bored();
    
    matrix_print_serial();
}

/*
 * Enter sleep mode
 */
void enter_sleep_mode() {
    is_sleeping = true;
    Serial.println("[Basal Ganglia] Entering sleep mode...");
    show_sleeping();
    matrix_print_serial();
}

/*
 * Exit sleep mode
 */
void exit_sleep_mode() {
    is_sleeping = false;
    idle_cycles = 0;
    dopamine_level = 0.5;
    Serial.println("[Basal Ganglia] Waking up...");
    show_neutral();
    matrix_print_serial();
}

/*
 * Send status to Dragonwing
 */
void send_status() {
    Serial.println("[Status]");
    Serial.print("dopamine:");
    Serial.println(dopamine_level, 4);
    Serial.print("idle_cycles:");
    Serial.println(idle_cycles);
    Serial.print("is_sleeping:");
    Serial.println(is_sleeping ? 1 : 0);
    Serial.print("activity:");
    Serial.println(brain.activity_counter);
    Serial.println("[/Status]");
}

/*
 * Process neural input
 */
void process_neural_input(String input) {
    // Simple hash-based input conversion
    fixed_t inputs[16];
    for (int i = 0; i < 16; i++) {
        inputs[i] = to_fixed(0.0);
    }
    
    // Parse input string into fixed-point values
    int idx = 0;
    int start = 0;
    for (int i = 0; i <= input.length() && idx < 16; i++) {
        if (i == input.length() || input.charAt(i) == ',') {
            String num = input.substring(start, i);
            num.trim();
            if (num.length() > 0) {
                float val = num.toFloat();
                inputs[idx] = to_fixed(val);
                idx++;
            }
            start = i + 1;
        }
    }
    
    // Process through network
    fixed_t* output = brain.forward(inputs);
    
    Serial.print("[Neural Output] ");
    for (int i = 0; i < 4; i++) {
        Serial.print(to_float(output[i]), 4);
        if (i < 3) Serial.print(", ");
    }
    Serial.println();
}

/*
 * Monitor activity and detect boredom
 */
void monitor_activity() {
    uint32_t now = millis();
    
    if (now - last_check_time > ACTIVITY_CHECK_INTERVAL) {
        last_check_time = now;
        
        if (now - last_activity_time > ACTIVITY_CHECK_INTERVAL) {
            idle_cycles++;
            dopamine_level = max(0.0, dopamine_level - DOPAMINE_DECAY_RATE);
            
            if (idle_cycles > BOREDOM_THRESHOLD && !is_sleeping) {
                trigger_boredom();
            }
        }
    }
}

/*
 * Trigger boredom behavior
 */
void trigger_boredom() {
    Serial.println("[Basal Ganglia] Boredom detected!");
    show_bored();
    matrix_print_serial();
    
    // Signal Dragonwing
    Serial.println("[Event] boredom");
}

/*
 * Trigger reflexive fear response
 */
void trigger_fear() {
    Serial.println("[Basal Ganglia] Fear reflex triggered!");
    show_fear();
    matrix_print_serial();
    
    // Signal Dragonwing
    Serial.println("[Event] fear");
}

/*
 * Main loop - Basal Ganglia coordination
 */
void loop() {
    if (!is_initialized) {
        return;
    }
    
    if (is_sleeping) {
        // Minimal processing during sleep
        check_dragonwing_input();
        delay(100);
        return;
    }
    
    // Check for input from Dragonwing
    check_dragonwing_input();
    
    // Monitor activity levels
    monitor_activity();
    
    // Small delay to prevent overwhelming
    delay(50);
}