// ==========================================
// C++ STL (STANDARD TEMPLATE LIBRARY) BASICS
// ==========================================
//
// --- QUICK DEFINITION ---
// The Standard Template Library (STL) is a library of pre-built, highly optimized data structures (like vectors, sets, maps) and algorithms (like sorting) in C++.
//
// --- REAL-WORLD USE CASES ---
// The Standard Template Library (STL) provides pre-built data structures and algorithms 
// so you don't have to build them from scratch.
// Examples:
//   * Dynamic Lists: Using std::vector to store an online shopping cart list that grows.
//   * Priority Tasks: Using std::queue to handle system printing tasks in order.
//   * Search Indexing: Using std::map (dictionary) to search users by user ID.
//

#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <set>
#include <map>
#include <algorithm> // Required for sort()
using namespace std;

int main() {
    // --- 1. Vectors (Dynamic Arrays that can grow/shrink in size) ---
    vector<int> numbers;
    numbers.push_back(10); // Adds 10 to the end
    numbers.push_back(20); // Adds 20 to the end
    numbers.push_back(5);  // Adds 5 to the end

    cout << "Vector size: " << numbers.size() << endl; // Output: Vector size: 3
    cout << "First element: " << numbers[0] << endl;   // Output: First element: 10

    // --- 2. Sorting (Pre-built quicksort utility) ---
    // Sorts elements in ascending order: [10, 20, 5] -> [5, 10, 20]
    sort(numbers.begin(), numbers.end());
    cout << "Sorted first element: " << numbers[0] << endl; // Output: Sorted first element: 5

    // --- 3. Stacks (LIFO - Last In, First Out) ---
    // Think of a stack of plates. You place new plates on top, and remove from the top.
    stack<int> plates;
    plates.push(1);
    plates.push(2);
    cout << "Top plate: " << plates.top() << endl; // Output: Top plate: 2
    plates.pop(); // Removes the top plate (2)
    cout << "New top plate: " << plates.top() << endl; // Output: New top plate: 1

    // --- 4. Queues (FIFO - First In, First Out) ---
    // Think of a line at a ticket counter. First person in line gets tickets first.
    queue<string> line;
    line.push("Alice");
    line.push("Bob");
    cout << "First in line: " << line.front() << endl; // Output: First in line: Alice
    line.pop(); // Removes Alice
    cout << "New first in line: " << line.front() << endl; // Output: New first in line: Bob

    // --- 5. Sets (Stores UNIQUE elements in sorted order) ---
    // Duplicates are automatically ignored.
    set<int> uniqueNumbers;
    uniqueNumbers.insert(5);
    uniqueNumbers.insert(10);
    uniqueNumbers.insert(5); // Duplicate, ignored!
    cout << "Set size: " << uniqueNumbers.size() << endl; // Output: Set size: 2

    // --- 6. Maps (Key-Value pairs / Dictionary) ---
    // Connects a key to a value (e.g. Roll Number -> Name)
    map<int, string> studentDb;
    studentDb[101] = "Sinha";
    studentDb[102] = "Raj";
    cout << "Student 101 Name: " << studentDb[101] << endl; // Output: Student 101 Name: Sinha

    return 0;
}

// ==========================================
// MNC INTERVIEW QUESTIONS & ANSWERS
// ==========================================
//
// ⭐ Q1. What is the difference between a Vector and a normal Array in C++?
// A:  A normal array has a fixed size defined at compilation and cannot change. 
//     A vector is a dynamic array that automatically resizes itself in memory 
//     when new elements are added or deleted.
//
// ⭐ Q2. How does std::set handle duplicate elements?
// A:  'std::set' stores only unique elements. If you attempt to insert an element 
//     that already exists in the set, the insertion is ignored and the size of 
//     the set remains unchanged.
//
// ⭐ Q3. What is the time complexity of searching an element in std::map vs std::unordered_map?
// A:  'std::map' is implemented as a Red-Black Tree, giving a search time complexity 
//     of O(log N). 'std::unordered_map' is implemented using Hash Tables, giving an 
//     average search time complexity of O(1) (constant time).
