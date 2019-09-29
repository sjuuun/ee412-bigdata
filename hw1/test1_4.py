import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split('\t|,', l))

total = len(split.collect())
#threshold = total // 100
threshold = 2
print "this is total\n"
print total
print threshold

freq = split.flatMap(lambda l: l) \
       .map(lambda s: (s,1)) \
       .reduceByKey(lambda n1, n2: n1 + n2) \
       .filter(lambda count: count[1] > threshold)

print freq.collect()

"""
def make_pair(x):
	result = [];    
	for i in x[1]:
		if i > x[0]:
			result.append((x[0], i));
	return result

pairs = split.flatMap(make_pair) \
	.collect()


def make_common(x):
        me = x[0]
        friends = x[1]
	result = []
	for i in range(len(friends)):
                if me < friends[i]:
                        result.append(((me, friends[i]), friends))
                else:
                        result.append(((friends[i], me), friends))
	return result	

def count_common(x):
        friends1 = x[0]
        friends2 = x[1]
        result = 0
        for i in friends1:
                if i in friends2:
                        result = result + 1
        return result
        

interest = split.flatMap(make_common) \
           .filter(lambda p: not(p[0] in pairs)) \
           .groupByKey() \
           .mapValues(list) \
           .map(lambda p: (p[0], count_common(p[1]))) \
           .sortByKey() \

"""        
#           .filter(lambda p: not (p in pairs)) \
#           .map(lambda p: (p, 1)) \
#           .reduceByKey(lambda n1, n2: count_common(n1, n2)) \
#           .map(lambda p: (p[0], len(p[1]))) \
#           .sortByKey()
"""

final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(10)

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()"""
