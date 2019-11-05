# Please check file name!! py2 or py3
import sys
from pyspark import SparkConf, SparkContext

# Get imput
f = open(sys.argv[1], 'r')

lines = sc.textFile(sys.argv[1])

