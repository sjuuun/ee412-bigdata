import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')

linesF = f.readlines()
pairs = []
genre = []

for line in linesF:
    tmp = re.split(',', line)
    movieID = int(tmp[0])
    clusters = re.split('\|', re.sub('\s+', '', tmp[-1]))
    for i in clusters:
        if i == '(nogenreslisted)':
            continue
        genre.append(i)
    pairs.append((movieID, clusters))
#print pairs
genre = list(set(genre))
print genre

def rmse(a,b):
    return np.sqrt(np.mean(np.square(np.array(a)-np.array(b))))

print rmse([1,2,3], [1,0,0])