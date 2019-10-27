import numpy as np

# Matrix of users and items
M = np.array([[1,1,1,0,0],[3,3,3,0,0],[4,4,4,0,0],[5,5,5,0,0],
             [0,0,0,4,4],[0,0,0,5,5],[0,0,0,2,2]])
M_norm = float(np.sum(np.square(M)))
print M
print M_norm

# select row and columns
row_select = [1,2]
col_select = [0,1]
r = 2

# Initialize C,R
C = np.zeros((M.shape[0], r))
R = np.zeros((r, M.shape[1]))

# Compute matrix C
for i in range(r):
    q = float(np.sum(np.square(M[:,col_select[i]])))
    weight = (r * (q/M_norm)) ** 0.5
    C[:,i] = M[:,col_select[i]] / weight
print C

# Compute matrix R
for i in range(r):
    q = float(np.sum(np.square(M[row_select[i],:])))
    weight = (r * (q/M_norm)) ** 0.5
    R[i,:] = M[row_select[i],:] / weight
print R