# Get user input
grade_input = input("Please enter your grade: ")

# Convert input to float
grade = float(grade_input)

# Determine and print the letter grade
if grade >= 90:
    print("A")
elif 80 <= grade < 90:
    print("B")
elif 70 <= grade < 80:
    print("C")
elif 60 <= grade < 70:
    print("D")
else:
    print("F")
