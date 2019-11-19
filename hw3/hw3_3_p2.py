import sys
import numpy as np
'''
# Get input
f = open(sys.argv[1], 'r')  # features.txt
q = open(sys.argv[2], 'r')  # labels.txt
features = f.readlines()
labels = q.readlines()

def make_set(x_list, y_list, num):
    assert(len(x_list) == len(y_list) == num)
    result = []
    for i in range(num):
        x = map(int, x_list[i].split(','))
        x.append(1)
        y = int(y_list[i])
        result.append((np.array(x), y))
    return result

# Divide data to 10 chunks
nset = 2
set_num = 4
test_set = []
train_sets = []
# Take first 600 data to test
test_set = make_set(features[:nset], labels[:nset], nset)
print (test_set)

# Take train sets
for i in range(1,set_num):
    feature = features[nset*i : nset*(i+1)]
    label = labels[nset*i : nset*(i+1)]
    train_sets.append(make_set(feature, label, nset))
print (train_sets)
'''
# SVM algorithm
C = 0.1
eta = 0.2
x_set = [(np.array([1,4,1]), 1), (np.array([2,2,1]), 1), (np.array([3,4,1]), 1), (np.array([1,1,1]), -1),
     (np.array([2,1,1]), -1), (np.array([3,1,1]), -1)]
w = np.array([0,1,-2])

def svm_train(C, eta, train_set, w):
    d_w = np.zeros(len(w))
    for i in range(len(train_set)):
        x = train_set[i]
        if (x[1] * np.dot(x[0], w) < 1):
            d_w += (-1)*x[1]*x[0]
    d_w = w + C*d_w
    return w - eta*d_w
    
for i in range(6):
    w = svm_train(C, eta, x_set, w)
    print w
