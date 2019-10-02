import numpy as np

test = np.zeros((2,1), int)

test[1] = 3
test = np.vstack([test, [0]])
print test

col = test.shape[1]
print col

hello = np.zeros((0,0))
print hello

hellw = np.zeros((0,1))
print hellw

lis = [1,2,3,4,5,5,1]
print list(set(lis))