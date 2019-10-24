import sys
#from pyspark import SparkConf, SparkContext

# Take input
f = open(sys.argv[1], 'r')
lines = f.readlines()
k_value = int(sys.argv[2])

## Implement the initialization of clusters
# make input to data sample
data = []
for line in lines:
    data.append(map(float, line.split(" ")))
#print data

def eu_distance(a, b):
    assert len(a) == len(b)
    sumsq = 0
    for i in range(len(a)):
        sumsq = sumsq + (a[i]-b[i])**2
    return sumsq ** 0.5
#for i in range(10):
#    print eu_distance(data[0], data[i])

def max_distance(points, q):
    max_dis = 0
    for p in points:
        dis = eu_distance(p, q)
        if max_dis < dis:
            max_dis = dis
            max_point = p
    return (points.index(max_point), max_dis)
#print "max distance"
#print max_distance(data, data[0])

def min_distance(points, q):
    min_dis = -1
    for p in points:
        dis = eu_distance(p, q)
        if (min_dis == -1) or (min_dis > dis):
            min_dis = dis
            min_point = p
    return (points.index(min_point), min_dis)
#print "min distance"
#print min_distance(data[1:], data[0])

# Initializing clusters for K-Means
centroid = []
centroid.append(data.pop(0))
while (len(centroid) < k_value):
    cent_dis = 0
    for p in data:
        dis = min_distance(centroid, p)[1]
        if cent_dis < dis:
            cent_dis = dis
            cent_point = p
    print data.index(cent_point)
    centroid.append(cent_point)
    data.remove(cent_point)
print centroid
print len(data)