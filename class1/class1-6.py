# Get user input
n = int(input("Enter a number: "))

# Validate input
if n < 1 or n > 11:
    print("Number too high, please enter a number between 1 and 11.")
else:
    # Print pyramid pattern
    for i in range(1, n + 1):
        print(str(i) * i)
