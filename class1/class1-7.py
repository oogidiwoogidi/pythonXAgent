# --- List Creation Examples ---
print([])  # This is an empty list
print([1, 2, 3])  # List with 3 elements
print([1, 2, 3, 4, 5])  # List with 5 elements
print([1, 2, 3, 4, 5, 6])  # List with 6 elements
print([1, 2, 3, 4, 5, 6, 7])  # List with 7 elements

# --- List Element Access (index starts from 0) ---
# This is the R in CRUD (Read)
L = [1, 2, 3, "a", "b", "c"]
print(L[0])  # First element
print(L[1])  # Second element
print(L[2])  # Third element
print(L[3])  # Fourth element

# --- List Slicing and Step ---
L = [1, 2, 3, "a", "b", "c"]
print(L[::2])  # Every second element, starting from index 0
print(L[1:4])  # Elements from index 1 to 3 (inclusive of 1, exclusive of 4)
print(L[1:4:2])  # Every second element from index 1 to 3

# --- List Length ---
L = [1, 2, 3, "a", "b", "c"]
print(len(L))  # Number of elements in the list

# --- List Iteration ---
# You can use the index to access data in the list,
# or directly iterate over the list elements.
L = [1, 2, 3, "a", "b", "c"]
for i in range(0, len(L), 2):
    print(L[i])  # Access elements using the index

# --- Call by Value ---
a = 1
b = a  # b is now a copy of a
b = 2  # Changing b does not affect a
print(a, b)

# --- Call by Reference ---
a = [1, 2, 3]
b = a  # b is now a reference to the same list as a
b[0] = 2  # Changing b affects a
print(a, b)  # Both a and b will show the change
b[0] = 2  # Changing b affects a
print(a, b)  # Both a and b will show the change

# --- Append to List ---
L = [1, 2, 3]
L.append(4)  # Adds 4 to the end of the list
print(L)  # Now L is [1, 2, 3, 4]

# --- Remove Elements from List ---
# 1. Use remove to delete a specified element
L = ["a", "b", "c", "d", "a"]
L.remove("a")  # Removes the first occurrence of "a"
# Use a loop to remove all occurrences of "a"
for i in L:
    if i == "a":
        L.remove(i)

# 2. Use pop to delete an element at a specified index
L = ["a", "b", "c", "d"]
L.pop(0)  # Removes the element at index 0 (the first element)
# pop removes the element at the specified index and returns it
# If no index is specified, pop removes the last element
L.pop()  # Removes the last element
print(L)  # Now L is ["b", "c", "d"]
L.pop()  # Removes the last element
print(L)  # Now L is ["b", "c", "d"]
