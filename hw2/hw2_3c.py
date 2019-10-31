import re
import sys
import random
import numpy as np

# Get input
f = open(sys.argv[1], 'r')  # ratings.txt
q = open(sys.argv[2], 'r')  # ratings_test.txt

linesF = f.readlines()
linesQ = q.readlines()
pairs = []                  # user and item pair of ratings.txt
test_pairs = []             # user and item pair of ratings_test.txt
user_list = []              # list of users
item_list = []              # list of items

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

# Make dictionary of user and item
# Its key is ID of user or item, and value is index of user of item in util_matrix
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

# Compute rmse of a and b
def rmse(a,b):
    if not np.any(a-b):
        return 0
    return np.sqrt(np.mean(np.square(np.array(a)-np.array(b))))

# Compute square sum of a-b (used in optimizing)
def error(a,b):
    return np.sum(np.square(a-b))

# Optimize U[i,j]
# M is norm_matrix, U is U matrix, V is V matrix
# Here, we optimize U[i,j]
def optimize_u(M, U, V, i, j):
    base = M[i,:]
    target = U[i,:]
    nonzero_index = np.where(base != 0)[0]
    start = -0.5
    d = 0.1
    target[j] += start
    err = error(base[nonzero_index], np.dot(target,V)[nonzero_index])
    for x in range(3):
        for _ in range(10):
            target[j] += d
            tmp = error(base[nonzero_index], np.dot(target,V)[nonzero_index])
            if tmp > err:
                target[j] -= d
                break
            err = tmp
        d *= 0.1
        start *= 0.1
        target[j] += start

# Optimize U[i,j]
# M is norm_matrix, U is U matrix, V is V matrix
# Here, we optimize V[i,j]
def optimize_v(M, U, V, i, j):
    base = M[:,j]
    target = V[:,j]
    nonzero_index = np.where(base != 0)[0]
    start = -0.5
    d = 0.1
    target[i] += start
    err = error(base[nonzero_index], np.dot(U,target)[nonzero_index])
    for x in range(3):
        for _ in range(10):
            target[i] += d
            tmp = error(base[nonzero_index], np.dot(U,target)[nonzero_index])
            if tmp > err:
                target[i] -= d
                break
            err = tmp
        d *= 0.1
        start *= 0.1
        target[i] += start

# Make U and V matrices
rank = 30
U = np.zeros((users, rank))
V = np.zeros((rank, items))

# Make train_pairs
# We will train U and V matrices with this pairs
# 0 means optimize with U, 1 means optimize V
train_pairs = []
for i in range(users):
    for j in range(rank):
        train_pairs.append((0,i,j))
for i in range(items):
    for j in range(rank):
        train_pairs.append((1,j,i))
#random.shuffle(train_pairs)

# Optimize UV decomposition
print len(train_pairs)
count = 0
for _ in range(1):
    random.shuffle(train_pairs)
    for x,i,j in train_pairs:
        if x == 0:
            optimize_u(norm_matrix,U,V,i,j)
        else:
            optimize_v(norm_matrix,U,V,i,j)
        count += 1
        if count % 10000 == 0:
            print count

print rmse(norm_matrix, np.dot(U,V))
print U

pred_matrix = np.dot(U,V)
# Write Result file
w = open("output.txt", 'w')
for pair in test_pairs:
    pred_user = int(pair[0])
    pred_item = int(pair[1])
    u_index = user_dic[pred_user]
    i_index = item_dic[pred_item]
    pred_rate = (norm_matrix[u_index, i_index] * user_std[u_index]) + user_avg[u_index]
    w.write(pair[0] + "," + pair[1] + "," + str(pred_rate) + "," + pair[-1])