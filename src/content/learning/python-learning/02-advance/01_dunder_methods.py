# ==========================================================
# PYTHON DUNDER METHODS & MAGIC (DEEPER PYTHON)
# ==========================================================

# --- WHAT ARE DUNDER METHODS? ---
# "Dunder" stands for Double Underscore (__) methods.
# They are also called "Magic Methods".
# You recognize them because they start and end with two underscores: e.g., __init__, __str__.
#
# These are special methods that Python calls under the hood when you perform certain actions.
# For example, when you run `len(my_list)`, Python actually calls `my_list.__len__()`.
# When you write `a + b`, Python calls `a.__add__(b)`.

# --- WHY USE THEM? ---
# They allow your custom classes to behave exactly like Python's built-in types (lists, integers, strings).
# This makes your code cleaner, more readable, and highly professional.

# ==========================================================
# 1. REPRESENTATION: __str__ vs __repr__
# ==========================================================
# When you print an object, Python needs to know how to display it.
# - __str__: Used for a user-friendly, readable text representation (what a user sees).
# - __repr__: Used for an unambiguous, developer-friendly representation (used for debugging).

class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    # Friendly string for printing to users
    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"

    # Developer representation (ideally shows how to recreate the object)
    def __repr__(self) -> str:
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"


print("--- 1. REPRESENTATION ---")
book = Book("Harry Potter", "J.K. Rowling", 323)

# Calls __str__
print("Using str():", str(book))
print("Printing object directly:", book)

# Calls __repr__
print("Using repr():", repr(book))
print()


# ==========================================================
# 2. OPERATOR OVERLOADING: __add__ & __eq__
# ==========================================================
# You can define what symbols like '+' or '==' do when used with your custom objects.

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # Defines behavior for the '+' operator
    def __add__(self, other: "Point") -> "Point":
        # Check if we are adding another Point
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    # Defines behavior for the '==' operator
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


print("--- 2. OPERATOR OVERLOADING ---")
p1 = Point(2, 4)
p2 = Point(1, 3)

# Python runs: p1.__add__(p2)
p3 = p1 + p2
print(f"{p1} + {p2} = {p3}")

# Python runs: p1.__eq__(p2)
print("Are p1 and p2 equal?", p1 == p2)
print("Is p1 equal to Point(2, 4)?", p1 == Point(2, 4))
print()


# ==========================================================
# 3. CONTAINER METHODS: __len__ & __getitem__
# ==========================================================
# You can make your object behave like a list or dictionary.

class Team:
    def __init__(self, name: str, members: list[str]):
        self.name = name
        self.members = members

    # Lets us use len(team)
    def __len__(self) -> int:
        return len(self.members)

    # Lets us use team[index]
    def __getitem__(self, index: int) -> str:
        return self.members[index]


print("--- 3. CONTAINER METHODS ---")
avengers = Team("Avengers", ["Iron Man", "Captain America", "Thor", "Hulk"])

# Python runs: avengers.__len__()
print(f"Number of members in {avengers.name}:", len(avengers))

# Python runs: avengers.__getitem__(0)
print("First member:", avengers[0])
print("Last member:", avengers[-1])
print()


# ==========================================================
# 4. CALLABLE OBJECTS: __call__
# ==========================================================
# You can make an instance of a class behave like a function that can be called!

class Greeter:
    def __init__(self, greeting_word: str):
        self.greeting_word = greeting_word

    # This makes the object call-able like a function
    def __call__(self, name: str) -> str:
        return f"{self.greeting_word}, {name}!"


print("--- 4. CALLABLE OBJECTS ---")
welcome = Greeter("Hello")
casual_greet = Greeter("Hey")

# We call the OBJECTS as if they were functions!
# Python runs: welcome.__call__("Alice")
print(welcome("Alice"))
print(casual_greet("Bob"))
print()


# ==========================================================
# QUICK CHALLENGE FOR YOU:
# ==========================================================
# Try creating a class `ShoppingBag` that has:
# - An `items` list.
# - A `__len__` method to return the count of items in the bag.
# - A `__str__` method to print a neat string: "Bag has items: [item1, item2...]"
# - An `__add__` method to merge two bags together!

class ShoppingBag:
    def __init__(self, items: list[str] = None):
        # Initialize with a list, or an empty list if None is passed
        self.items = items if items is not None else []

    # 1. __len__: returns the count of items in the bag
    def __len__(self) -> int:
        return len(self.items)

    # 2. __str__: returns a user-friendly string representation
    def __str__(self) -> str:
        return f"Bag has items: {self.items}"

    # 3. __add__: merges two bags together to return a new bag
    def __add__(self, other: "ShoppingBag") -> "ShoppingBag":
        if isinstance(other, ShoppingBag):
            # Merge both list of items and return a NEW ShoppingBag
            return ShoppingBag(self.items + other.items)
        return NotImplemented


print("--- CHALLENGE: SHOPPING BAG ---")
bag1 = ShoppingBag(["Apple", "Banana"])
bag2 = ShoppingBag(["Milk", "Bread", "Eggs"])

# Calls __str__ under the hood
print("Bag 1:", bag1)
print("Bag 2:", bag2)

# Calls __len__ under the hood
print("Number of items in Bag 1:", len(bag1))

# Calls __add__ under the hood
combined_bag = bag1 + bag2
print("Combined Bag:", combined_bag)
print("Total items in Combined Bag:", len(combined_bag))
print()

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Matrix Math Overloading: Customizing operations like matrix addition (+)
#    by overriding __add__.
#
# 2. Custom Collection APIs: Implementing custom list/dictionary classes with
#    length (__len__) and item lookup (__getitem__).
#
# 3. Object Debugging Logs: Providing clean string representations (__str__
#    and __repr__) for logging entities.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What are dunder (magic) methods in Python?
# A:  Dunder (Double Underscore) methods are special predefined methods in
#     Python that start and end with double underscores (like __init__,
#     __str__). They allow you to define custom behaviors that hook directly
#     into Python's built-in syntax (e.g. operator overloading, iteration).
#
# Q2. What is the difference between __str__ and __repr__?
# A:  `__str__` is designed to return a user-friendly, readable string
#     representation of the object (informal). `__repr__` (representation) is
#     designed to return an unambiguous, precise string representation that
#     ideally looks like the Python code used to recreate the object (formal).
#     When logging or debugging, developers use `__repr__` because it provides
#     precise type details, while `__str__` is displayed in user-facing
#     templates or prints. See the comparison table below:
#     
#     | Method | Intended Audience | Output Style | Called By |
#     | :--- | :--- | :--- | :--- |
#     | `__str__` | End-users | Readable / informal | `print()`, `str()` |
#     | `__repr__` | Developers | Precise / unambiguous | `repr()`, dev logs |
#
# Q3. How does Python implement operator overloading (e.g., adding two custom
#     objects)?
# A:  When Python evaluates a + b, it looks for the __add__ dunder method on
#     the left operand (a.__add__(b)). If a doesn't implement it, it tries
#     __radd__ on b. Implementing these methods inside your class enables
#     custom operator overloading.