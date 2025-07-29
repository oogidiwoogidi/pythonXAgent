# import random
import random as r

# random.randrange
# (random.reandrange() sets the range of numbers to choose from)
print(r.randrange(10))  # Random number between 0 and 9
print(r.randrange(1, 10))  # Random number between 1 and 9
print(r.randrange(1, 10, 2))  # Random odd number between 1 and 9
# random.randint
# (random.randint() requires both endpoints to be included)
# (the end number is inclusive)
print(r.randint(1, 10))  # Random number between 1 and 10
