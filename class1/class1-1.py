print("hello")
"""
this is a multi-line comment
you can write many things you want to remember in here 
these comments will not be executed by the program 
"""
# this is a single-line comment
# single-line comment are usually used to explain a specific line or section of code
# you can quickly add or remove single-line comments by using ctrl + /

# (basic data types)
print(1)  # integer
print(1.0)  # float
print("apple")  # string
print(True)  # boolean
print(False)  # boolean

# (Variables)
a = 10
# create a storage space named 'a', "=" assigns the value 10 on the right
# to 'a' on the left)
print(a)

# (operators)
print(a + 5)  # addition
print(a - 5)  # subtraction
print(a * 5)  # multiplication
print(a / 5)  # division'
print(a // 5)  # floor division
print(a % 5)  # Modulo
print(a**5)  # power

# (Priority)
# () Parentheses
# ** Power
# * / // % Multiplication, Division, Floor Division, Modulo
# + - Addition, Subtraction

# (string operations, +, *)
# (you can use + to concatenate strings and * to repeat them)
print("hello" + " world")  # concatenation
print("hello" * 3)  # repetition

# (string formatting)
name = "Elyas"
age = 12
print(f"My name is {name} and I am {age} years old")  # f-string formatting

# you can put variables or other data types into {} in f-strings to display
# them in the string

print(len(name))  # len()
# (len() is a funtion that can caculate the length of a string)
print(len(","))  # len()
# type() #check the type of a variable
print(type(1))  # <class 'int'>
print(type(1.0))  # <class 'float'>
print(type("apple"))  # <class 'str'>
print(type(True))  # <class 'bool'>

# (Type conversion)
print(int(1.5))  # convert float to int, result is 1
print(float(1))  # convert int to float, result is 1.0
print(str(1))  # convert int to string, result is "1"
print(bool(1))  # convert int to boolean, result is True
print(bool(0))  # convert int to boolean, result is False
print(float("1.5"))  # convert string to float, result is 1.5
print(int("1"))  # convert string to int, result is 1
print(str(True))  # convert boolean to string, result is "True"
print(str(False))  # convert boolean to string, result is "False"

print("start input")
# input (input()is a funtion that allows the user to input data)
# (the text inside the () is the prompt that will be displayed to the user)
a = input("Enter some text: ")
print("end input")
print(int(a) + 10)
print(type(a))
# (Proves that input() returns a string, even if the user inputs a number)
