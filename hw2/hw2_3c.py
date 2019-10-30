import re
import sys
import numpy as np

# Get input
f = open(sys.argv[1], 'r')  # ratings.txt
q = open(sys.argv[2], 'r')  # ratings_test.txt

lines = f.readlines()
pairs = []
user_list = []
item_list = []

for line in lines:
    tmp = re.split(',', line)[:-1]
    pairs.append([int(tmp[0]), int(tmp[1]), float(tmp[2])])
    user_list.append(int(tmp[0]))
    item_list.append(int(tmp[1]))
# Make distinct list
user_list = list(set(user_list))
item_list = list(set(item_list))
users = max(user_list)
items = max(item_list)