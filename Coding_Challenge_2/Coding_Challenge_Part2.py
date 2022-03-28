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

not_in_lists = []

for a in list_a:
    if a not in list_b:
        not_in_lists.append(a)
for b in list_b:
    if b not in list_a:
        not_in_lists.append(b)

not_in_both_lists = set(not_in_lists)
print(not_in_both_lists)