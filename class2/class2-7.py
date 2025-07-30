# try except (exception handiling structure)
# (error handling structure)
try:  # (try to execute code that may cause an error)
    n = int(input("input a number: "))  # Convert input to integer
except:  # (execute when an error is caught)
    print("you should input a number")


# (function definithon)
# (to define a new funtion , start with def , follow by the function name,
# to define a new function, start with def, followed by the function name,)
# parrentheses, and a colon.)
# (you can put parameters inside the parentheses or leave them empty.)
def hello():  # (defind a function wihtout parameters)
    print("Hello, world!")  # Print a message


for i in range(5):  # Loop 5 times
    hello()  # Call the hello function


# (funtion with parameters)
def greet(name):  # Define a function with a parameter
    print(f"Hello, {name}!")  # Print a greeting message


greet("Alice")  # Call the function with a name
greet("Bob")  # Call the function with another name
greet("Charlie")  # Call the function with yet another name
for i in range(3):  # Loop 3 times
    greet("Elyas")  # Call the function with a name


# (function with return value)
# (this funtion takes a number as input and returns its square)
# (the return statement is used to send a value back to the caller)
def add(a, b):  # Define a function with two parameters
    return a + b  # Return the sum of a and b


print(add(2, 3))  # Call the function with two numbers and print the result
print(
    add("Hello, ", "world!")
)  # Call the function with two strings and print the result
# (print the result of string connection)
sum = add(5, 10)  # Call the function and store the result in a variable
print(sum)  # Print the result stored in the variable


# (function with multiple return values)
# (this function takes two numbers and returns their sum and product)
def add_subtract(a, b):  # Define a function with two parameters
    return a + b, a - b  # Return both the sum and difference


sum, sub = add_subtract(10, 5)  # Call the function and unpack the returned values
print(f"Sum: {sum}, Subtraction: {sub}")  # Print the results


# (default parameters)
# (you cna set default values for parameters in a function)
# (when there are multiple parameters, the default value must be at the end)
def hello(name, message="Hello"):  # Define a function with a default parameter
    print(f"{message}, {name}!")  # Print a greeting message


hello("Alice")  # Call the function with one argument
hello("Bob", "Hi")  # Call the function with two arguments


# (type hinting)
# (you cna specify parameter types to hint what type shoe be passed)
def add(a: int, b: int) -> int:  # Define a function with type hints
    return a + b  # Return the sum of a and b


print(add(2, 3))  # Call the function with two integers
print(add("Hello, ", "world!"))  # Call the function with two strings (not recommended)

# (def local and global variables)
length = 10  # Global variable


def calculate_square_area(side_length):  # Function with a parameter
    area = side_length**2  # Local variable
    return area  # Return the area
    print(area)


length = 10  # Global variable
# caculate_square_area()  # Call the function with the global variable
# (the value of area is calculated when the function is called)


def calculate_square_area(side_length):  # Function with a parameter
    area = side_length**2  # Local variable
    # lenth is global area is local


calculate_square_area(length)  # Call the function with the global variable


def hello(name: str):  # Function with a type hint
    """
    (function description area)\n
    this is the function description area\n
    this is a greeting function\n
    (prarmeters)\n
    name: str - The name of the person to greet\n

    :none (returns: none)\n
    returns: None\n

    \n
    hello("alice") #hello, alice!\n(example: hello("alice") #hello, alice!)\n
    """
    print(f"hello, {name}!")  # Print a greeting message
