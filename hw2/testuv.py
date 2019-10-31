import numpy as np

M = [[1,2],[3,4]]
M = np.array(M)
I = np.ones((2,1))
J = np.ones((1,2))

def rmse(a,b):
    return np.sqrt(np.mean(np.square(np.array(a)-np.array(b))))

# Optimize U[i,j]
def optimize_u(M, U, V, i, j):
    base = M[i,:]
    target = U[i,:]
    nonzero_index = np.where(base != 0)
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
    nonzero_index = np.where(base != 0)
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

for _ in range(100):
    optimize_v(M,I,J,0,0)
    optimize_u(M,I,J,0,0)
    optimize_v(M,I,J,0,1)
    optimize_u(M,I,J,1,0)
    
print M
print I
print J
print np.dot(I,J)
print rmse(M, np.dot(I,J))

