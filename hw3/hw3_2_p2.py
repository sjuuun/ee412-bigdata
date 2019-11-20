import sys
from pyspark import SparkConf, SparkContext

# Get imput
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

pairs = lines.map(lambda line: line.split(','))