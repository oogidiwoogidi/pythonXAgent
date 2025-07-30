# open() (open() modes)
# r - read (read mode, file must exist)
# w - write (write mode, file will be created if it does not exist, existing content will be overwritten)
# a - append (append mode, file will be created if it does not exist, existing content will be preserved)
# r+ - read and write (read and write mode, file must exist)
# w+ - write and read (write and read mode, file will be created if it does not exist, existing content will be overwritten)
# a+ - append and read (append and read mode, file will be created if it

f = open("class1/class1-1.py", "r")  # Open file in read mode
content = f.read()  # Read file content
print(content)  # Print file content
f.close()  # Close the file

with open(
    "class1/class1-1.py", "r", encoding="utf-8"
) as f:  # Open file in read mode with UTF-8 encoding
    content = f.read()  # Read file content
    print(content)  # Print file content
    # f.close()  # No need to close the file, it will be closed automatically
    # (no need to write f.close() when using with statement)
