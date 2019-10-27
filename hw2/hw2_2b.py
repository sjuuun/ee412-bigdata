import numpy as np

M = np.array([[1,2,3],[3,4,5],[5,4,3],[0,2,4],[1,3,5]])
print "This is answer"
print np.linalg.svd(M)

# (a) Compute MTM and MMT.
MTM = np.dot(np.transpose(M), M)
MMT = np.dot(M, np.transpose(M))
print MTM
print MMT

# (b) Compute eigenpairs of MTM and MMT.
print "eigenpair of MTM"
MTM_pair = np.linalg.eig(MTM)
print MTM_pair
print "eigenpair of MMT"
MMT_pair = np.linalg.eig(MMT)
print MMT_pair

# (c) Find SVD (assume all eigenvalues are different)
rank = np.count_nonzero(MTM_pair[0].round(5))
print "This is rank"
print rank

eig_values = []
V = np.zeros((M.shape[1], rank))
U = np.zeros((M.shape[0], rank))
values = list(MTM_pair[0])

#print MTM_pair[1]
# Find V, which is matrix of eigenvectors of MTM
for i in range(rank):
    index = values.index(max(values))
    eig_values.append(values[index])
    values[index] = np.NINF
    V[:,i] = -MTM_pair[1][:,index]
    '''
    if MTM_pair[1][0,index] < 0:
        V[:,i] = -MTM_pair[1][:,index]
    else:
        V[:,i] = MTM_pair[1][:,index]
    '''
print V

# Find U, which is matrix of eigenvectors of MMT
values = list(MMT_pair[0])
for i in range(rank):
    index = values.index(max(values))
    values[index] = np.NINF
    U[:,i] = MMT_pair[1][:,index]
    '''
    if MMT_pair[1][0,index] < 0:
        U[:,i] = -MMT_pair[1][:,index]
    else:
        U[:,i] = MMT_pair[1][:,index]
    '''
print U

sigma = np.sqrt(np.diag(eig_values))
print sigma
#print np.dot(U,sigma)
print np.dot(np.dot(U,sigma), np.transpose(V))
