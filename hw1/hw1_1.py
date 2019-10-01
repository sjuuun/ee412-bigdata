import re
import sys
import numpy as np
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split(r'\t|,', l)) \
        .filter(lambda l: l[-1] != '')
 
#print "This is split"
#print split.collect()

def make_pair(x):
    who = x[0]
    friends = x[1:]
    result = []
    for i in range(len(friends)):
        result.append(((who, friends[i]), 0))
        for j in range(i+1, len(friends)):
            result.append(((friends[i], friends[j]), 1))
    return result

def count_common(n1, n2):
    if n1*n2 == 0:
        return 0
    else:
        return n1 + n2

pairs = split.flatMap(make_pair) \
        .reduceByKey(count_common) \
        .filter(lambda p: p[1] != 0)

final = pairs.map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .map(lambda x: (x[1], x[0])) \
        .take(10)

final = final.sort()
#print "Final"
#print final

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()
