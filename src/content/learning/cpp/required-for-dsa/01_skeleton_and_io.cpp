// ==========================================
// C++ SKELETON AND BASIC I/O
// ==========================================
//
// --- QUICK DEFINITION ---
// The skeleton is the basic boilerplate code required to compile and run any C++ program. 
// It imports standard input/output libraries to allow communication with the user.
//
// --- REAL-WORLD USE CASES ---
// 1. CONSOLE APPLICATIONS:
//    - **Step 1**: Command-line utilities that read user inputs.
//    - **Result**: Print output.
//
// 2. GAME LOGGERS:
//    - **Step 1**: Printing logs during game execution.
//    - **Result**: Debug events.
// --- HOW IT WORKS ---
// 1. #include <iostream>: Imports input/output stream library for cin/cout.
// 2. using namespace std: Avoids writing std:: before cout/cin.
// 3. int main(): The ignition key of your C++ program where execution starts.
//

#include <iostream>
using namespace std;

int main() {
    // 'cout' prints text to the screen. 
    // 'endl' inserts a newline and flushes the stream.
    cout << "Hello, Sinha!" << endl; // Output: Hello, Sinha!

    // '\n' is also used for a newline. It is generally faster than 'endl' because it doesn't force a stream flush.
    cout << "Welcome to the channel.\n"; // Output: Welcome to the channel.

    // You can also use a single character '\n' (very fast and clean).
    cout << '\n';

    // '\r' (Carriage Return) moves the cursor to the beginning of the line without going down.
    cout << "Loading: 50%\r";
    cout << "Loading: 100%\n"; // Output: Loading: 100% (this overwrote the 50% line!)

    // --- User Input (cin) ---
    int number;
    cout << "Enter a number: "; // Output: Enter a number:
    cin >> number;                             // (Assume user inputs: 10)
    cout << "You entered: " << number << endl; // Output: You entered: 10

    // --- Reading Multiple Inputs ---
    int x, y;
    cin >> x >> y; // (Assume user inputs: 10 12)
    cout << "Value of x: " << x << " and y: " << y << endl; // Output: Value of x: 10 and y: 12

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the difference between std::endl and '\n' in C++?
// A:  Both insert a newline. However, 'std::endl' also flushes the output buffer 
//     (writes immediately to the screen/file), which is a slow operation. 
//     '\n' just inserts the newline character without flushing, making it much faster.
//
// ⭐ Q2. Why is 'using namespace std;' considered bad practice in large projects?
// A:  It imports the entire standard namespace into the global namespace. This 
//     can cause naming collisions (e.g., if you define your own function named 
//     'count' and also use std::count). It is safer to use std::cout or specify 
//     the namespace explicitly.
//
// ⭐ Q3. What is '#include <bits/stdc++.h>' and when should you use it?
// A:  It is a non-standard header that includes all C++ standard library files. 
//     It is highly popular in competitive programming to save setup time, but 
//     should be avoided in production environments because it increases compilation 
//     times and isn't supported by all compilers.
