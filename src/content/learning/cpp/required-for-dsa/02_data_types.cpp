// ==========================================
// C++ DATA TYPES AND RANGES
// ==========================================
//
// --- QUICK DEFINITION ---
// Data types specify the type and size of values that variables can store (such as integers, decimals, characters, or text). This tells the compiler how much memory to allocate.
//
// --- REAL-WORLD USE CASES ---
// Data types define the type and size of data a variable can store. Examples:
//   * int / long: Storing counts, IDs, age.
//   * float / double: Storing financial prices, temperature, coordinates.
//   * char: Storing state flags ('Y'/'N'), grades ('A', 'B').
//   * string: Storing full names, emails, addresses.
//

#include <iostream>
#include <string>
using namespace std;

int main() {
    // --- 1. Integers (Whole Numbers) ---
    // 'int' stores whole numbers (usually 4 bytes, range: -10^9 to 10^9).
    int count = 100;

    // 'long' stores larger integers (usually 4 or 8 bytes, range: -10^12 to 10^12).
    long largeId = 123456789L;

    // 'long long' stores very large integers (8 bytes, range: -10^18 to 10^18).
    long long globalCount = 987654321012345LL;

    // --- 2. Decimals (Floating-Point Numbers) ---
    // 'float' stores single-precision decimal numbers (4 bytes, ends with 'f').
    float price = 19.99f;

    // 'double' stores double-precision decimal numbers (8 bytes, more precise).
    double preciseValue = 3.14159265358979;

    // --- 3. Characters ---
    // 'char' stores a single character enclosed in single quotes (1 byte).
    char symbol = '$';
    cout << "Symbol: " << symbol << endl; // Output: Symbol: $

    // --- 4. Strings & getline() ---
    // A string is a collection of characters enclosed in double quotes.
    // 'cin >>' only reads a string until the first whitespace.
    // To read an entire line (including spaces), use 'getline(cin, var)'.
    string sentence;
    cout << "Enter a full sentence: "; // Output: Enter a full sentence: 
    
    // Clear any remaining newline from the input buffer
    cin.ignore(); 
    getline(cin, sentence); // (Assume user inputs: Hello World from Sinha)
    cout << "Full sentence: " << sentence << endl; // Output: Full sentence: Hello World from Sinha

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the difference between float and double in C++?
// A:  'float' is a single-precision 32-bit type (gives ~7 decimal digits of accuracy).
//     'double' is a double-precision 64-bit type (gives ~15 decimal digits of accuracy).
//     Double is the default decimal type in C++ because of its superior precision.
//
// ⭐ Q2. How do cin >> str and getline(cin, str) differ when reading strings?
// A:  'cin >> str' reads input up to the first whitespace (space, tab, or newline).
//     'getline(cin, str)' reads the entire line of input, including spaces, until a newline 
//     character is encountered.
//
// ⭐ Q3. Why do we use cin.ignore() before calling getline()?
// A:  When reading data prior to 'getline()' using 'cin >>', a newline character ('\n') 
//     is often left behind in the input buffer. 'cin.ignore()' discards this newline, 
//     preventing 'getline()' from immediately exiting with an empty string.
