import sys
import numpy as np
from pyspark import SparkConf, SparkContext

# Take input
f = open(sys.argv[1], 'r')
lines = f.readlines()
k_value = int(sys.argv[2])

## Implement the initialization of clusters
# make input to data sample
data = []
for line in lines:
    data.append(list(map(float, line.split(" "))))

# Calculate Euclidean distance between two points
def eu_distance(a, b):
    assert len(a) == len(b)
    return np.linalg.norm(np.array(a)-np.array(b))

# Find the closest point from q, return its index and distance
def min_distance(points, q):
    min_dis = -1
    for p in points:
        dis = eu_distance(p, q)
        if (min_dis == -1) or (min_dis > dis):
            min_dis = dis
            min_index = points.index(p)
    return (min_index, min_dis)

## Initializing clusters for K-Means
centroid = [data[0]]

while (len(centroid) < k_value):
    cent_dis = 0
    for p in data:
        dis = min_distance(centroid, p)[1]
        if cent_dis < dis:
            cent_dis = dis
            cent_point = p
    centroid.append(cent_point)

## K-Means Clustering with Spark
conf = SparkConf()
sc = SparkContext(conf=conf)
D0 = sc.parallelize(data)

# Group by index of each centroids
clusters = D0.map(lambda p: (min_distance(centroid, p)[0], p)) \
            .groupByKey() \
            .mapValues(list) \
            .collect()

## Find average diameter
# Find furthest distance from q, return just distance
def max_distance(points, q):
    max_dis = 0
    for p in points:
        dis = eu_distance(p, q)
        if max_dis < dis:
            max_dis = dis
            max_point = p
    return max_dis

sum_dia = 0
for cluster in clusters:
    diameter = 0
    sets = cluster[1]
    for p in sets:
        tmp = max_distance(sets, p)
        if diameter < tmp:
            diameter = tmp
    sum_dia = sum_dia + diameter

# Print result
avg_dia = sum_dia / k_value
print ("k_value: %d, average diameter: %f" % (k_value, avg_dia))

