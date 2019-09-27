import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

def divide(x):
    for i in x[1]:
        (i, x[0])

words = lines.map(lambda l: re.split(r'\t', l)) \
        .map(lambda s: (s[0], re.split(r',', s[1]))) \
        .map(lambda x: divide(x)) \
        .collect()

print "Hello worls\n"

print words

sc.stop()
