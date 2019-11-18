import sys
from pyspark import SparkConf, SparkContext

# Get imput
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

# Split and mapping of transition matrix M
# (i,j) means Mji = 1
M = lines.map(lambda l: list(map(int, l.split())))

# Count how many times source appear
source = M.map(lambda pair: (pair[0], 1)) \
          .reduceByKey(lambda n1, n2: n1+n2) \
          .collect()
s_dic = {}
for s in source:
    s_dic[s[0]] = float(s[1])

# Initialize vector v, e, beta
v = [1/float(len(s_dic))] * len(s_dic)
beta = 0.9
e = (1-beta)/len(s_dic)

# Mapping in matrix multiplication
def multiple(pair):
    c, r = pair
    return (r, v[c-1]/s_dic[c])

# Texation: beta*M*v + (1-beta)*e/n
def texation(value):
    return beta*value + e

# Iterate 50 times
iter = 50
for _ in range(iter):
    mul = M.map(multiple) \
            .reduceByKey(lambda n1, n2: n1+n2) \
            .collect()
    # Sort ascending order according to row number
    mul.sort(key = lambda x: x[0])
    # Make new v
    v = [texation(x[1]) for x in mul]

# Result
# Question: how do we break tie?
pr = []
for i in range(len(v)):
    pr.append((i+1, v[i]))
pr.sort(key = lambda x: -x[1])
pr = pr[:10]
for top in pr:
    print("%d\t%.5f" % (top[0], top[1]))