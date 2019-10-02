import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split(r'\t|,', l)) \
        .filter(lambda l: l[-1] != '')

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

final = pairs.takeOrdered(10, key = lambda x: -x[1])

final.sort(key = lambda pair: (-pair[1], pair[0]))

for i in final:
	print "%s\t%s\t%d" % (i[0][0], i[0][1], i[1])


sc.stop()
