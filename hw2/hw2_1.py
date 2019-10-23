import sys
#from pyspark import SparkConf, SparkContext

# Take input
f = open(sys.argv[1], 'r')
lines = f.readlines()
#k_value = int(sys.argv[2])

## Implement the initialization of clusters
# make input to data sample
data = []
for line in lines:
    data.append(map(float, line.split(" ")))

print data