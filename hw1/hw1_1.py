import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])


split = lines.map(lambda l: re.split(r'\t', l)) \
        .filter(lambda l: len(l) > 1) \
        .map(lambda s: (s[0], re.split(r',', s[1]))) \
	.filter(lambda s: len(s[1]) > 1) \
	
pairs = split.flatMap(make_pair) \
	.collect()


final = interest.map(lambda i: (i[1], i[0])) \
        .sortByKey(False) \
        .take(10)

for i in final:
	print "%s\t%s\t%d" % (i[1][0], i[1][1], i[0])

sc.stop()
