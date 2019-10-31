import re
import sys
import numpy as np

# Get input
f = open(sys.argv[1], 'r')  # ratings.txt
q = open(sys.argv[2], 'r')  # ratings_test.txt

linesF = f.readlines()
linesQ = q.readlines()
pairs = []
test_pairs = []
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
    test_pairs.append(tmp)

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

# Noramlize util_matrix to norm_matrix
user_avg = np.zeros(users)
user_std = np.zeros(users)
for i in range(users):
    user_vector = np.copy(util_matrix[i,:])
    nonzero_index = np.where(user_vector != 0)[0]
    nonzero_num = len(nonzero_index)
    avg = np.mean(user_vector[nonzero_index])
    std = np.std(user_vector[nonzero_index])
    user_avg[i] = avg
    user_std[i] = std
    user_vector[nonzero_index] = (user_vector[nonzero_index] - avg) / std
    norm_matrix[i,:] = user_vector

w = open("output.txt", 'w')
for pair in test_pairs:
    pred_user = int(pair[0])
    pred_item = int(pair[1])
    u_index = user_dic[pred_user]
    i_index = item_dic[pred_item]
    print user_avg[u_index]
    pred_rate = (norm_matrix[u_index, i_index] * user_std[u_index]) + user_avg[u_index]
    w.write(pair[0] + "," + pair[1] + "," + str(pred_rate) + "," + pair[-1])