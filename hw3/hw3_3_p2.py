import sys
import numpy as np

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
nset = 600
set_num = 10
dim = 122
test_set = []
train_sets = []
# Take first 600 data to test
test_set = make_set(features[:nset], labels[:nset], nset)
#print (test_set)

# Take train sets
for i in range(1,set_num):
    feature = features[nset*i : nset*(i+1)]
    label = labels[nset*i : nset*(i+1)]
    train_sets.append(make_set(feature, label, nset))
#print (train_sets)


# SVM algorithm
C = 0.5
eta = 0.0001

'''
x_set = [(np.array([1,4,1]), 1), (np.array([2,2,1]), 1), (np.array([3,4,1]), 1), (np.array([1,1,1]), -1),
     (np.array([2,1,1]), -1), (np.array([3,1,1]), -1)]
w = np.array([0,1,-2])
'''

def svm_train(C, eta, train_set, w):
    d_w = np.zeros(len(w))
    for i in range(len(train_set)):
        x = train_set[i]
        # If y*(x*w) >= 1 then 0 else -y*x
        if (x[1] * np.dot(x[0], w) < 1):
            d_w += (-1)*x[1]*x[0]
    d_w = w + C*d_w
    return w - eta*d_w

def svm_test(test_set, w):
    correct = 0
    for x in test_set:
        # If sign of w*x + b and y are same, correct.
        if (x[1] * np.dot(x[0], w) >= 0):
            correct += 1
    return correct / float(len(test_set))

'''
for i in range(6):
    print svm_test(x_set, w)
    w = svm_train(C, eta, x_set, w)
    print w
'''
'''
w_last = np.ones(len(w))
iter = 0
while (np.linalg.norm(w - w_last) > 0.001):
    w_last = np.copy(w)
    w = svm_train(C, eta, x_set, w)
    if(iter % 1000 == 0):
        print w
        print w_last
        print np.linalg.norm(w - w_last)
    iter += 1
print svm_test(x_set, w)
'''

w = np.zeros(dim+1)
w_last = np.ones(dim+1)
while (np.linalg.norm(w - w_last) > 0.001):
    w_last = np.copy(w)
    for train in train_sets:
        w = svm_train(C, eta, train, w)

print svm_test(test_set, w)
