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
print pairs
#users.sort()
print users
#print len(users)
#print max(users)
#print items

# Construct utility matrix
util_matrix = np.zeros((len(users), len(items)))
for pair in pairs:
    util_matrix[users.index(pair[0])][items.index(pair[1])] = pair[2]
#print util_matrix

def cosine_distance(a, b):
    assert (len(a) == len(b))
    return np.sum(np.dot(a,b)) / \
            (np.linalg.norm(a) * np.linalg.norm(b))

