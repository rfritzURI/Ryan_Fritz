# 2. List overlap
# Using these lists:
#
# list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
# list_b = ['dog', 'hamster', 'snake']
# Determine which items are present in both lists.
# Determine which items do not overlap in the lists.

list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']
list_a_as_set = set(list_a)
intersection = list_a_as_set.intersection(list_b)
intersection_as_list = list(intersection)
print(intersection)