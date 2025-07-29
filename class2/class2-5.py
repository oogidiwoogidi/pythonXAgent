# Dictionary
# A dictionary stores data in key-value pairs. Keys are unique; values can repeat.
# Dictionaries are unordered, meaning the order of elements is not guaranteed.
# Dictionary keys must be immutable types, such as strings, numbers, or tuples.
# Dictionary values can be of any type, including lists, dictionaries, etc.
# Key-value pairs are separated by commas.

d = {
    "a": 1,
    "b": 2,
    "c": 3,
}  # Create a dictionary with keys "a", "b", "c" and their corresponding values

# Get all keys in the dictionary
print(d.keys())
for key in d.keys():  # Iterate through the keys
    print(key)  # Print key

# Get dictionary values
print(d.values())  # Get all values in the dictionary
for value in d.values():  # Iterate through the values
    print(value)  # Print value

# Get dictionary key-value pairs
print(d.items())  # Get all key-value pairs in the dictionary
for key, value in d.items():  # Iterate through the key-value pairs
    print(key, value)  # Print key and value

# Add/modify dictionary key-value pairs
d["d"] = 4  # Add a new key "d" with value 4
print(d)  # Now d is {"a": 1, "b": 2, "c": 3, "d": 4}
d["a"] = 5  # Modify the value of key "a" to 5
print(d)  # Now d is {"a": 5, "b": 2, "c": 3, "d": 4}

# Delete dictionary key-value pairs using pop
# If key exists, it will be deleted and the value will be returned
print(d.pop("a"))  # Delete key "a" and return its value
# If key does not exist, return the default value None
print(d.pop("x", None))  # Try to delete key "x", which does not exist, returns None
# If key does not exist and no default is provided, raises KeyError

# Check if key exists in dictionary
# "in" checks keys, not values
print("a" in d)  # Check if key "a" exists in the dictionary, returns True
print("e" in d)  # Check if key "e" exists in the dictionary

# (more complex dictionary)
d = {
    "a": [1, 2, 3],
    "b": {"c": 4, "d": 5},
}  # Create a dictionary with a list and another dictionary as values
print(d["a"])  # Access the list associated with key "a"
print(d["a"][0])  # Access the first element of the list associated with key "a"
# (get first element of the list associated with key "a")
print(d["b"])  # {'c': 4, 'd': 5}  # Access the dictionary associated with key "b"
print(d["b"]["c"])  # Access the value associated with key "c" in
# 4 key 'b'key key'c' (get value of key 'c')
