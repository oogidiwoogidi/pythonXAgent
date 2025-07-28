print("hello")
"""
This is a multi-line comment.
You can write anything you want to remember here.
These comments will not be executed by the program.
"""

# Single-line comments are usually used to explain a specific line or section of code.
# You can quickly add or remove single-line comments by using Ctrl + /.

# --- Basic Data Types ---
print(1)  # Integer
print(1.0)  # Float
print("apple")  # String
print(True)  # Boolean
print(False)  # Boolean

# --- Variables ---
a = 10
# Create a storage space named 'a'. "=" assigns the value 10 on the right to 'a' on the left.
print(a)

# --- Operators ---
print(a + 5)  # Addition
print(a - 5)  # Subtraction
print(a * 5)  # Multiplication
print(a / 5)  # Division
print(a // 5)  # Floor division
print(a % 5)  # Modulo
print(a**5)  # Power

# --- Operator Priority ---
# 1. () Parentheses
# 2. ** Power
# 3. * / // % Multiplication, Division, Floor Division, Modulo
# 4. + - Addition, Subtraction

# --- String Operations ---
# You can use + to concatenate strings and * to repeat them.
print("hello" + " world")  # Concatenation
print("hello" * 3)  # Repetition

# --- String Formatting ---
name = "Elyas"
age = 12
print(f"My name is {name} and I am {age} years old")  # f-string formatting
# You can put variables or other data types into {} in f-strings to display them in the string.

# --- Built-in Functions ---
print(len(name))  # len() calculates the length of a string
print(len(","))  # len()
print(type(1))  # <class 'int'>
print(type(1.0))  # <class 'float'>
print(type("apple"))  # <class 'str'>
print(type(True))  # <class 'bool'>

# --- Type Conversion ---
print(int(1.5))  # Convert float to int, result is 1
print(float(1))  # Convert int to float, result is 1.0
print(str(1))  # Convert int to string, result is "1"
print(bool(1))  # Convert int to boolean, result is True
print(bool(0))  # Convert int to boolean, result is False
print(float("1.5"))  # Convert string to float, result is 1.5
print(int("1"))  # Convert string to int, result is 1
print(str(True))  # Convert boolean to string, result is "True"
print(str(False))  # Convert boolean to string, result is "False"

# --- Input Example ---
print("start input")
# input() is a function that allows the user to input data.
# The text inside the parentheses is the prompt that will be displayed to the user.
a = input("Enter some text: ")
print("end input")
print(int(a) + 10)
print(type(a))
# Proves that input() returns a string, even if the user inputs a number.
print(int(a) + 10)
print(type(a))
# Proves that input() returns a string, even if the user inputs a number.
