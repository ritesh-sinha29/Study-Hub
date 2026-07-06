// ==========================================
// C++ FUNCTIONS: PASS BY VALUE AND REFERENCE
// ==========================================
//
// --- REAL-WORLD USE CASES ---
// Functions help split large codebases into modular, reusable blocks.
// Examples:
//   * Math Operations: Creating a function to compute factorials or exponents.
//   * Sorting Utilities: Reusable functions that sort any array passed to them.
//   * Data Modifiers: Updating user details in databases.
//
// --- HOW IT WORKS ---
// 1. Pass by Value: Passes a COPY of the variable. Changes inside do NOT affect the original.
// 2. Pass by Reference: Passes the memory reference of the original variable (uses '&').
//

#include <iostream>
using namespace std;

// --- 1. Pass by Value ---
// Passes a COPY of the variable. Changes inside the function do NOT affect the original.
void passByValue(int num) {
    num = 100;
}

// --- 2. Pass by Reference ---
// Passes the memory reference of the original variable (uses '&' symbol).
// Any changes made inside the function directly modify the original variable.
void passByReference(int &num) {
    num = 100;
}

int main() {
    int originalVal = 10;
    cout << "Original Value: " << originalVal << endl; // Output: 10

    // Call pass by value (passing a copy of originalVal)
    passByValue(originalVal);
    cout << "After Pass by Value: " << originalVal << endl; // Output: 10 (remains unchanged)

    // Call pass by reference (passing direct reference to originalVal)
    passByReference(originalVal);
    cout << "After Pass by Reference: " << originalVal << endl; // Output: 100 (changed!)

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the difference between Pass by Value and Pass by Reference?
// A:  * Pass by Value: Passes a copy of the argument. Modifications inside 
//       the function do not affect the original variable.
//     * Pass by Reference: Passes the memory address of the argument (using '&'). 
//       Any changes made to the parameter directly modify the original variable.
//
// ⭐ Q2. When should you prefer passing arguments by reference?
// A:  Prefer passing by reference when:
//     1. You need the function to modify the original variable.
//     2. Passing large structures or objects (like vectors or strings) to avoid the 
//        performance overhead of copying large amounts of data in memory.
//
// ⭐ Q3. How do you pass an object by reference but guarantee it won't be modified?
// A:  You can pass it by constant reference by adding the 'const' keyword before 
//     the reference parameter (e.g., 'void print(const string &str)'). This gives you 
//     the performance benefits of pass-by-reference without the risk of accidental modification.
