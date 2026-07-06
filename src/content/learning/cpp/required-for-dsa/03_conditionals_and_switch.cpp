// ==========================================
// C++ CONDITIONALS: IF-ELSE AND SWITCH
// ==========================================
//
// --- QUICK DEFINITION ---
// Conditionals (if-else, switch) are control flow statements that allow your program to make decisions and execute different blocks of code based on true or false conditions.
//
// --- REAL-WORLD USE CASES ---
// Conditionals are used to make decisions in code execution based on variables.
// Examples:
//   * Authentication: Check if username and password match database records.
//   * Menu Options: Choose actions (e.g., Press 1 to Save, Press 2 to Delete).
//   * Eligibility: Checking if a user's age is 18 or older to allow sign up.
//

#include <iostream>
using namespace std;

int main() {
    // --- 1. If-Else and Else-If Statements ---
    int marks = 85;

    // Check conditions sequentially. The first 'true' block will be executed.
    if (marks >= 90) {
        cout << "Grade: A+" << endl;
    } else if (marks >= 80) {
        cout << "Grade: A" << endl; // Output: Grade: A
    } else if (marks >= 50) {
        cout << "Grade: Pass" << endl;
    } else {
        cout << "Grade: Fail" << endl;
    }

    // --- 2. Nested If-Else Statements ---
    int age = 22;
    if (age >= 18) {
        // Nested block inside the parent 'if'
        if (age >= 60) {
            cout << "Senior citizen benefits applied." << endl;
        } else {
            cout << "Standard adult benefits applied." << endl; // Output: Standard adult benefits applied.
        }
    } else {
        cout << "Minor status." << endl;
    }

    // --- 3. Switch Case Statement ---
    // Switch evaluates a single expression and jumps directly to the matching case.
    // IMPORTANT: Always use 'break' to prevent execution from falling through to the next cases!
    int day = 3;
    switch (day) {
        case 1:
            cout << "Monday" << endl;
            break;
        case 2:
            cout << "Tuesday" << endl;
            break;
        case 3:
            cout << "Wednesday" << endl; // Output: Wednesday (Directly jumps here and outputs Wednesday)
            break;
        default:
            // Fallback case if no match is found
            cout << "Invalid day number!" << endl;
            break;
    }

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the role of the 'break' statement in a switch case?
// A:  The 'break' statement terminates the switch block immediately. If omitted, 
//     execution will continue (fall through) to subsequent cases and execute 
//     their code blocks regardless of whether they match the condition or not.
//
// ⭐ Q2. When should you prefer a switch statement over if-else ladders?
// A:  Prefer 'switch' when evaluating a single variable against multiple constant 
//     integral values (like integers or characters). Compilers optimize 'switch' 
//     using jump tables, making it faster than an if-else chain for large numbers of cases.
//
// ⭐ Q3. Can you use floating-point numbers (float/double) as a switch expression?
// A:  No. The switch expression must evaluate to an integral type (like int, char, 
//     short, long) or an enumeration. Floating-point numbers are not allowed because 
//     exact equality checks on decimals are unreliable due to rounding offsets.
