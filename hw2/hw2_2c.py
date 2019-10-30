import numpy as np

# Matrix of users and items
M = np.array([[1,1,1,0,0],[3,3,3,0,0],[4,4,4,0,0],[5,5,5,0,0],
             [0,0,0,4,4],[0,0,0,5,5],[0,0,0,2,2]])
M_norm = float(np.sum(np.square(M)))

# select row and columns
# (a) [1,2], [0,1] (b) [3,4] [1,2] (c) [0,6] [0,4]
row_select = [0,6]
col_select = [0,4]
r = np.linalg.matrix_rank(M)

# Initialize C,U,R
C = np.zeros((M.shape[0], r))
U = np.zeros((r,r))
R = np.zeros((r, M.shape[1]))

# Compute matrix C
for i in range(r):
    q = float(np.sum(np.square(M[:,col_select[i]])))
    weight = (r * (q/M_norm)) ** 0.5
    C[:,i] = M[:,col_select[i]] / weight
print (C)

# Compute matrix R
for i in range(r):
    q = float(np.sum(np.square(M[row_select[i],:])))
    weight = (r * (q/M_norm)) ** 0.5
    R[i,:] = M[row_select[i],:] / weight
print (R)

# Compute matrix U
W = np.zeros((r,r))
for i in range(r):
    for j in range(r):
        W[i,j] = M[row_select[i], col_select[j]]
W_rank = np.linalg.matrix_rank(W)
WTW_pair = np.linalg.eig(np.dot(np.transpose(W), W))
WWT_pair = np.linalg.eig(np.dot(W, np.transpose(W)))
X = np.zeros((r,W_rank))
Y = np.zeros((r,W_rank))
eig_values = []

values = list(WTW_pair[0])
for i in range(W_rank):
    index = values.index(max(values))
    eig_values.append(values[index])
    values[index] = 0
    Y[:,i] = WTW_pair[1][:,index]
if Y[0,0] < 0:
    Y = -Y

values = list(WWT_pair[0])
for i in range(W_rank):
    index = values.index(max(values))
    values[index] = 0
    X[:,i] = WWT_pair[1][:,index]
if X[0,0] < 0:
    X = -X

sigma = np.sqrt(np.diag(eig_values))
inverse_sigma = np.linalg.pinv(sigma)

U = np.dot(np.dot(np.dot(Y,inverse_sigma), inverse_sigma), np.transpose(X))
print (U)

#print (np.dot(np.dot(C,U), R))
