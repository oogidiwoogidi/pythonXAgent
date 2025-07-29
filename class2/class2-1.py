# --- Sorting Lists ---
# sort: sorts the elements in ascending order
# note: this method modifies the list in place; it does not create a new list
L = [1, 2, 3, 4, 5]
L.sort()  # Sorts the list in ascending order
print(L)  # Now L is [1, 2, 3, 4, 5]

# sort from largest to smallest (descending order)
L.sort(reverse=True)  # Sorts the list in descending order
print(L)  # Now L is [5, 4, 3, 2, 1]

# --- Arithmetic Assignment Operators ---
a = 1
a += 1  # Equivalent to a = a + 1
print(a)  # Now a is 2
a -= 1  # Equivalent to a = a - 1
print(a)  # Now a is 1
a *= 2  # Equivalent to a = a * 2
print(a)  # Now a is 2
a /= 2  # Equivalent to a = a / 2
print(a)  # Now a is 1.0
a //= 2  # Equivalent to a = a // 2
print(a)  # Now a is 0.0
a %= 2  # Equivalent to a = a % 2
print(a)  # Now a is 0.0
a **= 2  # Equivalent to a = a ** 2
print(a)  # Now a is 0.0

# --- Operator Precedence ---
# 1. () Parentheses
# 2. ** Power
# 3. * / // % Multiplication, Division, Floor Division, Modulo
# 4. + - Addition, Subtraction
# 5. == != < > <= >= Comparison
# 6. not
# 7. and
# 8. or
# 9. = += -= *= /= //= %= **= Assignment

# --- While Loop ---
# while: loop until a condition is met
# while condition: do something
# The loop will continue until the condition is false.
# After each iteration, the condition is checked again.
i = 0
while i < 5:  # Loop while i is less than 5
    print(i)  # Print the current value of i
    i += 1  # Increment i by 1

# --- Break Statement ---
# break: force exit the loop
# break exits the innermost loop it belongs to
i = 0
while i < 5:
    print(i)
    i += 1

# --- For Loop with Break ---
for j in range(5):
    print(j)
    if j == 3:  # If j is equal to 3
        break  # Exit the loop

for i in range(5):
    print(i)  # Print the current value of i
    if i == 3:  # If i is equal to 3
        break  # Exit the loop
