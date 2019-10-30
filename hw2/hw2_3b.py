import re
import sys
import numpy as np

# Get input, and make user list and item list
f = open(sys.argv[1], 'r')
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

# Construct utility matrix
util_matrix = np.zeros((users + 1, items + 1))

for pair in pairs:
    util_matrix[pair[0], pair[1]] = pair[2]

# Normalize utility matrix
norm_matrix = np.zeros((users + 1, items + 1))
norm_avg = np.zeros(users + 1)
for i in user_list:
    user_vector = np.copy(util_matrix[i,:])
    nonzero_index = np.where(user_vector != 0)[0]
    nonzero_num = len(nonzero_index)
    avg = sum(user_vector[nonzero_index]) / nonzero_num
    norm_avg[i] = avg
    user_vector[nonzero_index] -= avg
    norm_matrix[i,:] = user_vector

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
for i in user_list:
    if i == U:
        continue
    user_distance.append((i, cosine_distance(norm_matrix[U,:], norm_matrix[i,:])))
user_distance.sort(key = lambda x: -x[1])
similar_users = np.array([x[0] for x in user_distance[:10]])

predict_user_base = []
for i in range(1, 1001):
    # If no one rate item, pass
    if not i in item_list:
        continue
    nonzero_index = np.where(util_matrix[similar_users,i] != 0)[0]
    nonzero_num = len(nonzero_index)
    # If any similar user doesn't rate item, pass
    if nonzero_num == 0:
        continue
    predict_user_base.append((i, np.sum(norm_matrix[similar_users[nonzero_index],i]) / nonzero_num))
predict_user_base.sort(key = lambda x: -x[1])
predict_user_base = predict_user_base[:5]

print ("The result of prediction user-based")
for x in predict_user_base:
    print ("%d\t%f" % (x[0], x[1] + norm_avg[U]))

## Predict ratings using the user-based method
# The movie whose ratings will be predicted.
predict_item_base = []
for M in range(1, 1001):
    if not M in item_list:
        continue

    # Take top 10 similar item
    item_distance = []
    for i in item_list:
        if i == M:
            continue
        item_distance.append((i, cosine_distance(norm_matrix[:,M], norm_matrix[:,i])))
    item_distance.sort(key = lambda x: -x[1])
    similar_items = np.array([x[0] for x in item_distance[:10]])
    #print similar_items
    
    nonzero_index = np.where(util_matrix[U,similar_items] != 0)[0]
    nonzero_num = len(nonzero_index)
    # If user doesn't rate to all similar items, pass
    if nonzero_num == 0:
        continue
    predict_item_base.append((M, np.sum(norm_matrix[U,similar_items[nonzero_index]]) / nonzero_num))

predict_item_base.sort(key = lambda x: -x[1])
predict_item_base = predict_item_base[:5]

print ("The result of prediction item-based")
for x in predict_item_base:
    print ("%d\t%f" % (x[0], x[1] + norm_avg[U]))