// ==========================================
// C++ LOOPS: FOR AND WHILE
// ==========================================
//
// --- QUICK DEFINITION ---
// Loops (for, while) are structures used to repeat a block of code multiple times until a specific condition is met, preventing you from writing repetitive instructions.
//
// --- REAL-WORLD USE CASES ---
// Loops are used to repeat a block of code multiple times.
// Examples:
//   * Repeating tasks: Checking for new notifications every few seconds.
//   * Array Traversal: Summing up values inside an array.
//   * Game Loops: Keep rendering frames until the user presses the 'Exit' button.
//

#include <iostream>
using namespace std;

int main() {
    // --- 1. For Loop (Used when number of iterations is known beforehand) ---
    // Syntax: for(initialization; condition; increment/decrement)
    // 'i' starts at 1, loop runs as long as i <= 3, i increases by 1 each time.
    cout << "For loop counting forward:" << endl; // Output: For loop counting forward:
    for (int i = 1; i <= 3; i++) {
        cout << i << " "; // Output: 1 2 3
    }
    cout << endl;

    // --- 2. Reverse Loops ---
    cout << "For loop counting backward:" << endl; // Output: For loop counting backward:
    for (int i = 3; i >= 1; i--) {
        cout << i << " "; // Output: 3 2 1
    }
    cout << endl;

    // --- 3. While Loop (Used when number of iterations depends on a condition) ---
    int count = 1;
    cout << "While loop counting forward:" << endl; // Output: While loop counting forward:
    while (count <= 3) {
        cout << count << " "; // Output: 1 2 3
        count++; // Remember to update condition variable to avoid infinite loop!
    }
    cout << endl;

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the scope of a loop variable defined inside a for loop?
// A:  A variable declared in the initialization section of a for loop (e.g. 'int i = 0') 
//     has block scope. It is only accessible within the for loop block and is 
//     destroyed immediately after the loop terminates.
//
// ⭐ Q2. What is an infinite loop and how does it happen?
// A:  An infinite loop is a loop that repeats indefinitely because its termination 
//     condition always evaluates to true. This typically happens when the developer 
//     forgets to update the loop control variable (e.g. forgetting 'count++') inside 
//     the loop body.
//
// ⭐ Q3. What is the difference between a while loop and a do-while loop?
// A:  A 'while' loop checks the condition before executing the loop body (pre-test). 
//     If the condition is initially false, the loop body never runs. 
//     A 'do-while' loop executes the loop body first and checks the condition after 
//     (post-test), guaranteeing the loop body will run at least once.
