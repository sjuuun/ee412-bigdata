import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

def divide(x):
	result = [];    
	for i in x[1]:
		result.append((i, x[0]));
	return result

pairs = lines.map(lambda l: re.split(r'\t', l)) \
        .filter(lambda l: len(l) > 1) \
        .map(lambda s: (s[0], re.split(r',', s[1]))) \
	.flatMap(divide)

pair_list = pairs.collect()

common = pairs.groupByKey() \
         .mapValues(list)

def make_interest(x):
	people = x[1]
	result = []
	for i in range(len(people)):
		for j in (range(i+1, len(people))):
			result.append((people[i], people[j]))
	return result	

interest = common.flatMap(make_interest) \
           .filter(lambda p: not (p in pair_list)) \
           .map(lambda p: (p, 1)) \
           .reduceByKey(lambda n1, n2: n1 + n2) \
           .sortByKey()

final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(10)

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()
