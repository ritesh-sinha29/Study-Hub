// ========================================================================================
// GUARDRAILS & ROBUST INPUT VALIDATION (C++)
// ========================================================================================
//
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// SECTION 1 — C++ GUARDRAIL PATTERNS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//
// In systems programming and low-level development, guardrails prevent undefined behavior,
// buffer overflows, memory corruption, and application crashes. C++ provides mechanisms
// for safety checks at both compile-time and runtime.
//
// 1. RUNTIME STREAM VALIDATION: Check state flags of input streams (like std::cin) to handle
//    invalid user data gracefully and avoid infinite input loops.
// 2. RUNTIME BOUNDS CHECKS: Employs safe accessor functions (e.g. std::vector::at) instead of
//    unsafe subscript operators ([]) which bypass index verification.
// 3. COMPILE-TIME GUARDRAILS: Uses static assertions and templates to reject invalid types
//    or incorrect constant expressions before the compiler produces machine code.
//
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// SECTION 2 — C++ MEMORY & INPUT SECURITY FLOW
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//
//    Raw CLI Input ──► [ stream.fail() check ] ──(Invalid)──► [ clear() / ignore() ] ──► Retry
//                             │
//                          (Valid)
//                             ▼
//                   [ Array Index Access ] ───(Out of bounds)───► [ throw std::out_of_range ]
//                             │
//                           (Safe)
//                             ▼
//                     Execute Operation
//
// ========================================================================================

#include <iostream>
#include <vector>
#include <stdexcept>
#include <cassert>
#include <type_traits>

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 1. COMPILE-TIME GUARDRAIL (static_assert)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Prevents instantiating templates with unsafe or unsupported data types.

template <typename T>
struct NumericBuffer {
    // Compile-time guard: Ensure the buffer only holds numeric values
    static_assert(std::is_arithmetic<T>::value, "NumericBuffer can only store arithmetic types (ints/floats)!");
    
    std::vector<T> data;
    
    void add(T val) {
        data.push_back(val);
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 2. RUNTIME ACCESS GUARDRAIL (Safe Vector Read)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Validates boundaries when accessing sequential containers.

void safe_vector_read() {
    std::cout << "--- 1. RUNTIME ACCESS GUARDRAILS ---\n";
    std::vector<int> numbers = {10, 20, 30};

    // Unsafe: numbers[5] leads to Undefined Behavior (reads garbage or segmentation faults)
    // Safe: numbers.at(5) throws std::out_of_range exception
    
    try {
        std::cout << "  Attempting to read out-of-bounds index 5:\n";
        int value = numbers.at(5); 
        std::cout << "  Value: " << value << "\n";
    } catch (const std::out_of_range& e) {
        std::cout << "  [Guardrail] Access Blocked! Exception caught: " << e.what() << "\n";
    }
    std::cout << "\n";
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 3. RUNTIME INPUT STREAM GUARDRAIL (std::cin protection)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Handles situations where incorrect types are supplied to the terminal.

void safe_numeric_input() {
    std::cout << "--- 2. INPUT STREAM GUARDRAILS ---\n";
    int choice = 0;
    
    // Simulating safe input parsing
    std::cout << "  (Simulation) Enter an integer choice (inputting 'abc' triggers guardrail):\n";
    
    // Mocking an input event. For demo, we clear flags to simulate a recovery
    // if a previous scan failed.
    if (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(1000, '\n');
    }
    
    // Standard template for handling console reading failure:
    /*
    while (!(std::cin >> choice)) {
        std::cout << "  [Guardrail] ERROR: Invalid input type. Please enter a valid integer.\n";
        std::cin.clear(); // Clear stream fail states
        std::cin.ignore(1000, '\n'); // Discard invalid characters
    }
    */
    
    std::cout << "  Valid choice parsed successfully (Defaulted to choice = " << choice << ").\n\n";
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 4. RUNTIME DEBUG ASSERTIONS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Assertions are active in debug builds but disabled in release builds (-DNDEBUG).

void process_transaction(double amount) {
    // Guardrail: Assert amount is positive in test environments
    assert(amount > 0.0 && "Transaction amount must be positive!");
    std::cout << "  Processing transaction of $" << amount << "\n";
}

int main() {
    std::cout << "======================================================================\n";
    std::cout << "TESTING C++ COMPILE-TIME AND RUNTIME GUARDRAILS\n";
    std::cout << "======================================================================\n\n";

    // Test 1: Safe bounds read
    safe_vector_read();

    // Test 2: Input sanitization simulation
    safe_numeric_input();

    // Test 3: Static assertion (Compile time check)
    // Un-commenting the line below will trigger a compile-time compiler error!
    // NumericBuffer<std::string> stringBuffer; // Compiler will fail here
    
    NumericBuffer<double> doubleBuffer; // OK: double is arithmetic
    doubleBuffer.add(45.5);
    std::cout << "--- 3. COMPILE-TIME GUARDRAILS ---\n";
    std::cout << "  NumericBuffer compiled successfully for arithmetic types!\n\n";

    // Test 4: Runtime debug assertion
    std::cout << "--- 4. DEBUG ASSERTIONS ---\n";
    process_transaction(99.95);
    // process_transaction(-5.00); // Un-commenting this triggers assert failure at runtime

    return 0;
}

// ========================================================================================
// REAL-LIFE USE CASES
// ========================================================================================
//
// 1. EMBEDDED FLIGHT CONTROL:
//    - **Input**: Sensor arrays streaming coordinates or speed floats to thruster controllers.
//    - **Step 1**: Bounds guards (`std::vector::at()`) verify that index reads stay inside array sizes.
//    - **Step 2**: Safety functions evaluate coordinate vectors and disable engines if boundary checks fail.
//    - **Result**: Protects drone/spacecraft hardware from sudden crashes due to memory index corruption.
//
// 2. COMPILE-TIME MATRIX COMPUTATION:
//    - **Input**: Matrix multiplication template arguments defining matrix dimensions.
//    - **Step 1**: `static_assert` verifies matching inner dimensions at compile time.
//    - **Step 2**: The compiler fails compile-time checks instantly if matrices are incompatible.
//    - **Result**: Guarantees dimension safety before binary files are built or deployed.
//
// ========================================================================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ========================================================================================
//
// Q1. What is the key difference between std::vector::operator[] and std::vector::at()?
// A:  `operator[]` does not perform boundary checks. If the index is out of bounds, it leads
//     to Undefined Behavior (UB), which could read memory silently, corrupt data, or crash.
//     `at()` performs boundary checking at runtime, throwing a `std::out_of_range` exception 
//     if index validation fails, which can be safely caught.
//
// Q2. When should you use static_assert vs runtime exceptions?
// A:  `static_assert` should be used to enforce constraints that can be determined at compile-time
//     (e.g., type matching, template parameter requirements, struct size alignments). Runtime
//     exceptions (`std::runtime_error`) should be used for errors that depend on runtime variables,
//     like user console inputs, missing files, or network connection state.
//
// Q3. What happens to standard assert() checks in release configurations?
// A:  Standard assertions (`assert()`) are disabled if the macro `NDEBUG` is defined at compile-time
//     (which is standard for release configurations). Therefore, assertions should be used strictly
//     for debugging code assumptions, never for checking operational runtime bounds (like file loading
//     success) because they are stripped out in release builds.
