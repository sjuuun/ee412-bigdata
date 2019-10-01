import re
import sys
import numpy as np
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split('\t|,', l)) \
        .collect()
        #lines.map(lambda l: re.split(r'\t', l)) \
        #.map(lambda s: (s[0], re.split(r',', s[1]))) \
        #.collect()
	    #.filter(lambda l: len(l) > 1) \
        # #.filter(lambda s: len(s[1]) > 1) \
print split
numPeople = len(split)

print "How many people"
print numPeople

# Make path(friends) matrix
friendMat = np.zeros((numPeople, numPeople))

for i in range(numPeople):
    friends = split[i][1:]
    for j in friends:
        friendMat[i][int(j)] += 1

print "Matrix of friend"
print friendMat

multi = sc.parallelize(friendMat) \
        .collect()

print "This is multi"
print multi
"""
pairs = split.flatMap(make_pair) \
	.collect()


final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(10)

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])
"""

sc.stop()
