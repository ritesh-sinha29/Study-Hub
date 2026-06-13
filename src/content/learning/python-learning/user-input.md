# User Input

## PYTHON USER INPUT (FOR BEGINNERS)

## REAL-WORLD USE CASES

Use the `input()` function when you need your program to interact with a human 
and collect information from them.
Examples:
  * User Login: Asking for a username and password.
  * Command Line Calculators: Asking the user to input two numbers to add.
  * Interactive Games: Asking "Do you want to play again? (yes/no)".

In Python, the `input()` function lets the program wait and ask the user to type something.
IMPORTANT: Whatever the user types is ALWAYS treated as a String (text) by default.

## Example 1: Asking for Text

Here, we ask the user for their name and print a greeting.

```python
name = input("Enter your name: ")
print("Hello,", name)      
print()
```

## Example 2: Asking for Numbers

Because `input()` always returns a string, we cannot do math directly with it.
E.g., if you input "8" and try to add 6, you will get an error.
We must convert the string to an integer (number) using `int()` first. This is called Type Casting.

```python
a = input("Enter a number to add 6 to it: ")
```

Convert `a` from text to an integer number, then add 6:

```python
result = int(a) + 6
print("Your number + 6 is:", result)```
```

