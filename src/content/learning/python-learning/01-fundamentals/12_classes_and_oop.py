# ==========================================
# PYTHON CLASSES & OOP (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A CLASS? ---
# A class is like a BLUEPRINT or TEMPLATE for creating objects.
# Example: A "Car" blueprint defines: color, brand, speed.
#          From that blueprint, you can create many actual cars.

# --- REAL-WORLD USE CASES ---
# * FastAPI + Pydantic: You define a `class User` as a model,
#   and FastAPI uses it to validate request and response data.
# * LangGraph: State objects that hold data as an agent runs are classes.
# * Everywhere: Grouping related data and behavior together.

print("==========================================")
print("1. CREATING A CLASS AND ITS OBJECTS")
print("==========================================")

# Step 1: Define the blueprint (Class)
class Dog:
    # __init__ is the constructor. It runs automatically when we create an object.
    # self represents the specific object we are creating.
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says: Woof!")


# Step 2: Create the actual Objects (also called Instances)
# Syntax: object_name = ClassName(arguments)
# When we call Dog("Bruno", "Labrador"), Python automatically calls __init__ behind the scenes.

dog1 = Dog("Bruno", "Labrador")  # Created object 1 (dog1)
dog2 = Dog("Max", "Pug")         # Created object 2 (dog2)

# Step 3: Access attributes and methods of the objects
print("Dog 1 name:", dog1.name)
print("Dog 2 breed:", dog2.breed)
dog1.bark()
dog2.bark()

# ==========================================
print("2. CLASS WITH MULTIPLE METHODS")
print("==========================================")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance   # starting balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"Deposited Rs.{amount}. New balance: Rs.{self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Not enough money!")
        else:
            self.balance = self.balance - amount
            print(f"Withdrew Rs.{amount}. New balance: Rs.{self.balance}")

    def show_balance(self):
        print(f"Account owner: {self.owner} | Balance: Rs.{self.balance}")

account = BankAccount("Ritesh", 5000)
account.show_balance()
account.deposit(2000)
account.withdraw(1000)
account.withdraw(10000)  # Should show "Not enough money!"

print()

# ==========================================
print("3. INHERITANCE — One class inherits from another")
print("==========================================")

# Think of it like a Parent and Child:
# 1. The Parent has some skills/possessions.
# 2. The Child inherits them automatically (gets them for free!).
# 3. The Child can also add their own skills, or "override" the Parent's skills.

# --- 3A. Simple Inheritance ---
class Parent:
    def __init__(self, surname):
        self.surname = surname

    def drive(self):
        print("Driving the family car.")

# Child inherits from Parent by putting Parent in parentheses: Child(Parent)
class Child(Parent):
    def play_games(self):
        print("Playing video games.")

# Let's test the Child:
kid = Child("Sinha")
print("--- 3A. Basic Inheritance ---")
print(f"Child's surname is: {kid.surname}")  # Inherited surname attribute!
kid.drive()                                   # Inherited drive method!
kid.play_games()                              # Child's own method!
print()

# --- 3B. Method Overriding ---
# When the Child changes a skill they inherited from the Parent:
class ChildWhoCooks(Parent):
    # Overriding the drive method to do it differently
    def drive(self):
        print("Driving a sports car very fast!")

cook_kid = ChildWhoCooks("Sinha")
print("--- 3B. Method Overriding ---")
cook_kid.drive()  # Uses the overridden version, not the parent's version
print()

# --- 3C. Using super() ---
# When the Child wants to do something but also call the Parent's version first:
class SmartChild(Parent):
    def __init__(self, surname, school):
        # Call the parent's __init__ to handle the surname
        super().__init__(surname)
        # Handle the new attribute
        self.school = school

    def drive(self):
        # Run the parent's drive method first, then add more stuff!
        super().drive()
        print("But driving very carefully because I'm a student.")

smart_kid = SmartChild("Sinha", "High School")
print("--- 3C. Using super() ---")
print(f"Smart kid's school is: {smart_kid.school}")
smart_kid.drive()
print()

# ==========================================
print("4. FASTAPI USE CASE — Pydantic Model (class)")
print("==========================================")

# In FastAPI, you define what data your API expects using a class.
# This is called a Pydantic model. It looks exactly like a normal class.

# (In real FastAPI: from pydantic import BaseModel)
# Here we simulate it without installing FastAPI:

class UserRequest:
    # This class represents the data a user sends when registering
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def to_dict(self):
        # FastAPI converts this to a JSON response automatically
        return {"name": self.name, "age": self.age, "email": self.email}

new_user = UserRequest("Ritesh", 20, "ritesh@example.com")
print("New user data:", new_user.to_dict())
