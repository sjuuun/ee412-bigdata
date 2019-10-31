import re
import sys
import random
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

#print (np.linalg.matrix_rank(util_matrix))

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
'''
print np.shape(norm_matrix)
U,S,Vt = np.linalg.svd(norm_matrix, full_matrices=False)
print np.shape(U)
print np.shape(S)
print np.shape(Vt)

#pred_matrix = np.dot(np.dot(U[:,:-1], np.diag(S[:-1])), Vt[:-1,:])
pred_matrix = np.dot(U, Vt)

print rmse(norm_matrix, pred_matrix)
'''
def rmse(a,b):
    if not np.any(a-b):
        return 0
    return np.sqrt(np.mean(np.square(np.array(a)-np.array(b))))

# Optimize U[i,j]
def optimize_u(M, U, V, i, j):
    base = M[i,:]
    target = U[i,:]
    nonzero_index = np.where(base != 0)[0]
    start = -0.5
    d = 0.1
    target[j] += start
    err = rmse(base[nonzero_index], np.dot(target,V)[nonzero_index])
    for x in range(3):
        for _ in range(10):
            target[j] += d
            tmp = rmse(base[nonzero_index], np.dot(target,V)[nonzero_index])
            if tmp > err:
                target [j] -= d
                break
            err = tmp
        d *= 0.1

# Optimize U[i,j]
def optimize_v(M, U, V, i, j):
    base = M[:,j]
    target = V[:,j]
    nonzero_index = np.where(base != 0)[0]
    start = -0.5
    d = 0.1
    target[i] += start
    err = rmse(base[nonzero_index], np.dot(U,target)[nonzero_index])
    for x in range(3):
        for _ in range(10):
            target[i] += d
            tmp = rmse(base[nonzero_index], np.dot(target,V)[nonzero_index])
            if tmp > err:
                target [i] -= d
                break
            err = tmp
        d *= 0.1

U = np.zeros((users, 100))
V = np.zeros((100, items))
train_pairs = []
for i in range(users):
    for j in range(items):
        if (util_matrix[i,j] == 0):
            continue
        train_pairs.append((i,j))
random.shuffle(train_pairs)

for x in range(100):
    for i,j in train_pairs:
        optimize_u(norm_matrix,U,V,i,x)
        optimize_v(norm_matrix,U,V,x,j)
    print x
    print rmse(norm_matrix, np.dot(U,V))

print rmse(norm_matrix, np.dot(U,V))
