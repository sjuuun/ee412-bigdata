import re
import sys
import numpy as np
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split('\t|,', l)) \
        .collect()
        #.collect()
        #lines.map(lambda l: re.split(r'\t', l)) \
        #.map(lambda s: (s[0], re.split(r',', s[1]))) \
        #.collect()
	    #.filter(lambda l: len(l) > 1) \
        # #.filter(lambda s: len(s[1]) > 1) \

#numPeople = int(max(max(split))) + 1
numPeople = 50000

#print "How many people"
#print numPeople

# Make path(friends) matrix
friendMat = np.zeros((numPeople, numPeople))

for i in range(numPeople):
    friends = split[i][1:]
    for j in friends:
        friendMat[i][int(j)] += 1

#print "Matrix of friend"
#print friendMat

# make (index, value) pair
def make_pair(x):
    pairs = []
    for i in range(len(x)):
        pairs.append((i, int(x[i])))
    return pairs

# multiplication of symmetric matrix
def matrix_multiple(x):
    value = []
    for i in x:
        for j in x:
            value.append(((i[0],j[0]), i[1]*j[1]))
    return value

multi = sc.parallelize(friendMat) \
        .map(make_pair) \
        .flatMap(matrix_multiple) \
        .reduceByKey(lambda n1, n2: n1 + n2) \
        .filter(lambda x: x[0][0] < x[0][1]) \
        .filter(lambda x: friendMat[x[0][0]][x[0][1]] == 0) \
        .sortByKey()

#print "This is multi"
#print multi.collect()

final = multi.map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .take(10)

#print "Final"
#print final

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])


sc.stop()
