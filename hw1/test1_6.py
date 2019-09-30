import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

"""
def make_pair(x):
	result = [];    
	for i in x[1]:
		if i > x[0]:
			result.append((x[0], i));
	return result
"""

split = lines.map(lambda l: re.split(r'\t', l)) \
        .filter(lambda l: len(l) > 1) \
        .map(lambda s: (s[0], re.split(r',', s[1]))) \
        .sortByKey()
	#.filter(lambda s: len(s[1]) > 1) \
	
pairs = split.collect()

print pairs
print pairs[1]
print '3' in pairs[1]

def make_interest(x):
	people = x[1]
	result = []
	print people
	for i in range(len(people)-1):
		friends = pairs[int(people[i])][1]
		print "my friends"
		print friends
		for j in (range(i+1, len(people))):
			if (not (j in friends)):
				print j
				result.append((people[i], people[j]))
	return result	

interest = split.flatMap(make_interest) \
           .map(lambda p: (p, 1)) \
           .reduceByKey(lambda n1, n2: n1 + n2) \
           .sortByKey()
           #.filter(lambda p: not (p in pairs)) \

final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(10)

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()
