import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

split = lines.map(lambda l: re.split('\t|,', l))

total = len(split.collect())
#threshold = total // 100
threshold = 0
print "this is total\n"
print total
print threshold

freq = split.flatMap(lambda l: l) \
       .map(lambda s: (s,1)) \
       .reduceByKey(lambda n1, n2: n1 + n2) \
       .filter(lambda count: count[1] > threshold) \
       .flatMap(lambda t: t[0]) \
       .collect()

print "This is freq list"
print freq

def make_pair(x):
	result = [];    
	for i in x[1:]:
		if i > x[0]:
			result.append((x[0], i));
	return result

	
pairs = split.filter(lambda l: len(l) > 1) \
        .flatMap(make_pair) \
	.collect()

print "I'm pairs"
print pairs
#pair_list = pairs.collect()

#common = pairs.groupByKey() \
#         .mapValues(list)

def make_interest(x):
	people = x[1:]
	result = []
	for i in range(len(people)):
		for j in (range(i+1, len(people))):
			if (people[i] in freq) and (people[j] in freq):
				result.append((people[i], people[j]))
	return result	

interest = split.filter(lambda l: len(l) > 2) \
           .flatMap(make_interest) \
           .filter(lambda p: not (p in pairs)) \
           .map(lambda p: (p, 1)) \
           .reduceByKey(lambda n1, n2: n1 + n2) \
           .sortByKey()

print "interest"
print interest.collect()

final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(5)

print "final"
print final

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()
