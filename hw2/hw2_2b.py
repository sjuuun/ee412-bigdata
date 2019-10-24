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
print np.linalg.eig(MTM)
print "eigenpair of MMT"
print np.linalg.eig(MMT)

# (c) Find SVD
Sig = []

