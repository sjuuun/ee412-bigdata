import re
import sys
import numpy as np

# Get input, and make user list and item list
f = open(sys.argv[1], 'r')
lines = f.readlines()
pairs = []
users = []
items = []

for line in lines:
    tmp = re.split(',', line)[:-1]
    pairs.append(tmp)
    users.append(tmp[0])
    items.append(tmp[1])
users = list(set(users))
items = list(set(items))
#print pairs
#users.sort()
#print users
#print len(users)
#items.sort()
#print items
#print len(items)
#print max(users)
#print items

# Construct utility matrix
util_matrix = np.zeros((len(users), len(items)))
for pair in pairs:
    util_matrix[users.index(pair[0]),items.index(pair[1])] = pair[2]
#print util_matrix

# Normalize utility matrix
users_avg = []
for i in range(len(users)):
    avg = sum(util_matrix[i][:]) / np.count_nonzero(util_matrix[i,:])
    users_avg.append(avg)
    for j in range(len(items)):
        # Normalize for nonzero elements
        if util_matrix[i,j] != 0:
            util_matrix[i,j] -= avg
#print util_matrix

# Return cosine distance of a and b
def cosine_distance(a, b):
    assert (len(a) == len(b))
    return np.sum(np.dot(a,b)) / (np.linalg.norm(a) * np.linalg.norm(b))

# The user whose ratings will be predicted.
U = str(600)
U_index = users.index(U)

## Predict ratings using the user-based method
user_distance = []
for i in range(len(users)):
    if i == U_index:
        continue
    user_distance.append((i, cosine_distance(util_matrix[U_index,:], util_matrix[i][:])))
user_distance.sort(key = lambda x: -x[1])
# Index list of the 10 most similar users, which is used in util_matrix
similar_users = [x[0] for x in user_distance[:10]]
print similar_users

# Should be removed!!!!
# Print top 10 users for test
for sim in similar_users:
    print users[sim]

predict_user_base = []
for i in range(1, 1001):
    if not str(i) in items:
        continue
    index = items.index(str(i))
    sum = 0
    for sim in similar_users:
        sum += util_matrix[sim,index]
    predict_user_base.append((i, sum / 10))
predict_user_base.sort(key = lambda x: -x[1])
predict_user_base = predict_user_base[:5]
#print predict_user_base

for x in predict_user_base:
    print "%d\t%f" % (x[0], x[1] + users_avg[U_index])