// ==========================================
// TIME AND SPACE COMPLEXITY
// ==========================================

// --- REAL-WORLD USE CASES ---
// Complexity analysis is the language of algorithm performance. It helps you:
//   * Performance Tuning: Predict how slow an app will run when processing millions of users.
//   * Code Comparison: Decide which sorting algorithm is faster before shipping it.
//   * Resource Planning: Calculate how much server RAM (Space Complexity) is needed for database logs.

#include <iostream>
#include <vector>

using namespace std;

// --- 1. Constant Time: O(1) ---
// The execution time does not depend on the input size N. It is instantaneous.
void printFirstElement(const vector<int> &arr) {
    if (!arr.empty()) {
        cout << "First Element: " << arr[0] << endl; // Executed only once
    }
}

// --- 2. Linear Time: O(N) ---
// The execution time grows proportionally to the input size N.
void printAllElements(const vector<int> &arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) { // Loop runs N times
        cout << arr[i] << " ";
    }
    cout << endl;
}

// --- 3. Quadratic Time: O(N^2) ---
// Typically seen in nested loops. Execution time grows as N squared.
void printAllPairs(const vector<int> &arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {       // Runs N times
        for (int j = 0; j < n; j++) {   // Runs N times for each outer loop
            cout << "(" << arr[i] << ", " << arr[j] << ") ";
        }
    }
    cout << endl;
}

int main() {
    vector<int> sampleArr = {1, 2, 3};

    cout << "Running constant time O(1):" << endl;
    printFirstElement(sampleArr); // Output: First Element: 1

    cout << "\nRunning linear time O(N):" << endl;
    printAllElements(sampleArr); // Output: 1 2 3 

    cout << "\nRunning quadratic time O(N^2):" << endl;
    printAllPairs(sampleArr); // Output: (1, 1) (1, 2) (1, 3) (2, 1) ...

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is Big-O notation?
// A:  Big-O notation is a mathematical notation used to describe the upper bound 
//     (worst-case scenario) of an algorithm's running time or space requirements 
//     relative to the input size N.
//
// ⭐ Q2. What is the difference between Time Complexity and Space Complexity?
// A:  * Time Complexity: Measures the rate at which an algorithm's execution time 
//       increases as the input size grows.
//     * Space Complexity: Measures the extra memory/RAM space required by the 
//       algorithm to run to completion, relative to the input size.
//
// ⭐ Q3. Why is O(log N) complexity considered highly efficient?
// A:  O(log N) (logarithmic time) means the search space is cut in half at each step 
//     (like Binary Search). Even for an input size N of 1 million elements, an O(log N) 
//     algorithm will complete in approximately 20 operations, making it extremely fast.
