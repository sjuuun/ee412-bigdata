import re
import sys
import numpy as np

# Get input, and make user list and item list
f = open(sys.argv[1], 'r')
lines = f.readlines()
pairs = []

for line in lines:
    tmp = re.split(',', line)[:-1]
    pairs.append([int(tmp[0]), int(tmp[1]), float(tmp[2])])
#print pairs
users = max(x[0] for x in pairs)
items = max(x[1] for x in pairs)

# Construct utility matrix
util_matrix = np.zeros((users + 1, items + 1))

for pair in pairs:
    util_matrix[pair[0], pair[1]] = pair[2]
print ("Construct Done")

# Normalize utility matrix
norm_matrix = np.zeros((users + 1, items + 1))
norm_avg = [0]  # dump value
for i in range(1, users + 1):
    # Pass if user vector is zero vector
    user_vector = np.copy(util_matrix[i,:])
    nonzero_index = np.where(user_vector != 0)[0]
    nonzero_num = len(nonzero_index)
    if nonzero_num == 0:
        norm_avg.append(0)
        continue
    avg = sum(user_vector[nonzero_index]) / nonzero_num
    norm_avg.append(avg)
    user_vector[nonzero_index] -= avg
    norm_matrix[i,:] = user_vector
#print np.count_nonzero(util_matrix - norm_matrix)
print ("Normalize Done")
#print len(norm_avg)

# Return cosine distance of a and b
def cosine_distance(a, b):
    assert (len(a) == len(b))
    product = np.dot(a,b)
    if product == 0:
        return 0
    else:
        return product / (np.linalg.norm(a) * np.linalg.norm(b))

## Predict ratings using the user-based method
# The user whose ratings will be predicted.
U = 600

# Take top 10 similar user
user_distance = []
for i in range(1, users+1):
    if i == U:
        continue
    user_distance.append((i, cosine_distance(norm_matrix[U,:], norm_matrix[i,:])))
user_distance.sort(key = lambda x: -x[1])
similar_users = np.array([x[0] for x in user_distance[:10]])
print similar_users

predict_user_base = []
for i in range(1, 1001):
    # If no one rate item, pass
    if np.count_nonzero(util_matrix[:,i]) == 0:
        continue
    nonzero_index = np.where(util_matrix[similar_users,i] != 0)[0]
    nonzero_num = len(nonzero_index)
    # If any similar user doesn't rate item, pass
    if nonzero_num == 0:
        continue
    predict_user_base.append((i, np.sum(norm_matrix[similar_users[nonzero_index],i]) / nonzero_num))
predict_user_base.sort(key = lambda x: -x[1])
predict_user_base = predict_user_base[:5]

print "The result of prediction user-based"
for x in predict_user_base:
    print "%d\t%f" % (x[0], x[1] + norm_avg[U])
'''
# Return cosine distance of a and b
def cosine_distance(a, b):
    assert (len(a) == len(b))
    return np.sum(np.dot(a,b)) / (np.linalg.norm(a) * np.linalg.norm(b))

# list of (movie_ID, predicted rating)
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

print "The result of prediction user-based"
for x in predict_user_base:
    print "%d\t%f" % (x[0], x[1]) #+ users_avg[U_index])


## Predict ratings using the item-based method
'''