# Comparison operators
print(1 == 1)  # True, equal
print(1 != 2)  # True, not equal
print(1 < 2)  # True, less than
print(2 > 1)  # True, greater than
print(1 <= 1)  # True, less than or equal to
print(2 >= 1)  # True, greater than or equal to

# Logical operators
# and: both conditions must be true
print(True and True)  # True
print(True and False)  # False
print(False and True)  # False
print(False and False)  # False

# or: at least one condition must be true
print(True or True)  # True
print(True or False)  # True
print(False or True)  # True
print(False or False)  # False

# not: negates the condition
print(not True)  # False
print(not False)  # True

# Operator precedence (from highest to lowest)
# 1. () (parentheses)
# 2. ** (power)
# 3. * / // % (multiplication, division, floor division, modulo)
# 4. + - (addition, subtraction)
# 5. == != < > <= >= (comparison operators)
# 6. not
# 7. and
# 8. or

# Password gate check
password = input("Enter your password: ")
if password == "1234":
    print("Welcome Elyas")
elif password == "12345":
    print("Welcome Adena")
elif password == "123456":
    print("Welcome Vincent")
elif password == "1234567":
    print("Welcome Jovy")
else:
    print("Wrong password")
