# 1. List values
# Using this list:
#
# [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
# Make a new list that has all the elements less than 5 from this list in it and print out this new list.
# Write this in one line of Python (you do not need to append to a list just print the output).
# You should have two solutions in this file, one for item 1 and one for item 2. Item 2 is tricky so if you get stuck
# try your best (no penalty), for a hint check out the solution by desiato here.

# # list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
for i in list:

    if i < 5:

        print(i)

# Using list-comprehension:

x=[i for i in list if i <5]
print(x)