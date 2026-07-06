// ==========================================
// C++ ARRAYS AND STRINGS
// ==========================================
//
// --- REAL-WORLD USE CASES ---
// Arrays and Strings are basic containers used to store collection of elements sequentially.
// Examples:
//   * Chessboards: 2D array of size 8x8 storing chess pieces.
//   * Lists of Marks: Storing student test marks.
//   * Text Processing: Storing and parsing string tokens like words or commands.
//

#include <iostream>
#include <string>
using namespace std;

int main() {
    // --- 1. One-Dimensional Arrays ---
    // Arrays store fixed-size elements of the same type in contiguous memory locations.
    // Indexing starts at 0 (first element: scores[0], last element: scores[size-1]).
    int scores[3] = {90, 85, 95};
    
    // Modify array elements directly
    scores[1] = 88;
    cout << "First score: " << scores[0] << endl; // Output: First score: 90
    cout << "Second score (modified): " << scores[1] << endl; // Output: Second score (modified): 88

    // --- 2. Two-Dimensional Arrays (Matrices) ---
    // Declared as arrayName[rows][columns]. Great for grids and graph representations.
    int matrix[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    cout << "Element at row 1, col 2: " << matrix[1][2] << endl; // Output: Element at row 1, col 2: 6

    // --- 3. Strings as Indexable Containers ---
    // A string is essentially an array of characters. 
    // You can access and modify individual characters by index.
    string text = "Sinha";
    cout << "First character: " << text[0] << endl; // Output: First character: S

    // Get length using size() or length()
    cout << "String size: " << text.size() << endl; // Output: String size: 5

    // Modify a character (use single quotes for char)
    text[0] = 's';
    cout << "Modified string: " << text << endl; // Output: Modified string: sinha

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What does it mean that array elements are stored in contiguous memory?
// A:  It means that elements are placed back-to-back in the computer's memory. 
//     For example, if the first element of an integer array (4 bytes each) is at 
//     memory address 1000, the next element is guaranteed to be at address 1004, 
//     the third at 1008, and so on.
//
// ⭐ Q2. Why do C++ array indexes start from 0 instead of 1?
// A:  The index represents the memory offset (distance) from the starting address 
//     of the array. The first element sits exactly at the starting memory address, 
//     so its offset/distance from the start is 0.
//
// ⭐ Q3. What happens if you try to access an index out of bounds in C++?
// A:  C++ does not perform runtime array boundary checks. Accessing an out-of-bounds 
//     index (e.g., scores[5] in an array of size 3) results in undefined behavior. 
//     It will read or overwrite garbage memory, leading to bugs or segmentation faults.
