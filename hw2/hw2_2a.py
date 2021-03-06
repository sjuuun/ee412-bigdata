import numpy as np

M = np.array([[1,1,1],[1,2,3],[1,3,6]])

# Finding eigenpairs by power iteration.
for i in range(3):
    x = np.ones((3,1))
    tmp = np.zeros((3,1))

    while (np.linalg.norm(x-tmp) > 0.0001):
        tmp = x
        product = np.dot(M, x)
        x = product / np.linalg.norm(product)
    eig_value = np.dot(np.dot(np.transpose(x), M), x)
    M = M - eig_value*np.dot(x, np.transpose(x))
    print ("eig_value: %f" % eig_value)
    print (x)
    print (M)
