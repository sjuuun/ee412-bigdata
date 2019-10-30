import re
import sys
import numpy as np

# Get input
f = open(sys.argv[1], 'r')  # ratings.txt
q = open(sys.argv[2], 'r')  # ratings_test.txt

linesF = f.readlines()
linesQ = q.readlines()
pairs = []
user_list = []
item_list = []

# Input from ratings.txt
for line in linesF:
    tmp = re.split(',', line)[:-1]
    pairs.append([int(tmp[0]), int(tmp[1]), float(tmp[2])])
    user_list.append(int(tmp[0]))
    item_list.append(int(tmp[1]))

# Input from ratings_test.txt
for line in linesQ:
    tmp = re.split(',', line)
    user_list.append(int(tmp[0]))
    item_list.append(int(tmp[1]))

# Make distinct list
user_list = list(set(user_list))
item_list = list(set(item_list))
users = len(user_list)
items = len(item_list)

user_dic = {}
item_dic = {}
for i in range(users):
    user_dic[user_list[i]] = i
for i in range(items):
    item_dic[item_list[i]] = i

util_matrix = np.zeros((users, items))
norm_matrix = np.zeros((users, items))

for pair in pairs:
    util_matrix[user_dic[pair[0]], item_dic[pair[1]]] = pair[2]
