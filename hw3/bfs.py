import sys
from pyspark import SparkConf, SparkContext

# Get imput
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

pair = lines.map(lambda line: tuple(map(int, line.split(','))))

adjList = pair.groupByKey() \
               .mapValues(list) \
               .collect()
adjPoint = {}
for adj in adjList:
    adjPoint[adj[0]] = adj[1]
print adjPoint

# Define class
DONE = 0
DIST = 1
WEIGHT = 2
PATH = 3

def bfs_init((src, dst)):
    return ((src, dst), [0,1,1,[[src]]])

def bfs_left((K, V)):
    return not V[DONE]

def bfs_adj(path, adj):
    flatten = [y for x in path for y in x]
    flatten = list(set(flatten))
    return [p for p in adj if not(p in flatten)]

def bfs_next(data, target):
    (src, dst), [done, dist, weight, path] = data
    dist += 1
    path = [p + [dst] for p in path]
    return ((src, target), [done, dist, weight, path])

def bfs_map(data):
    K,V = data
    if V[DONE]:
        return [data]
    else:
        adj = bfs_adj(V[PATH], adjPoint[K[1]])
        result = [bfs_next(data, p) for p in adj]
        V[DONE] = 1
        return [data] + result

def bfs_reduce(V1, V2):
    if V1[DIST] < V2[DIST]:
        return V1
    elif V1[DIST] > V2[DIST]:
        return V2
    else:
        assert(V1[DIST] == V2[DIST])
        w = V1[WEIGHT] + V2[WEIGHT]
        path = V1[PATH] + V2[PATH]
        return [V1[0], V1[1], w, path]

def bfs_edge(path, dst):
    edge = []
    for i in range(len(path)-1):
        edge.append((path[i], path[i+1]))
    edge.append((path[-1], dst))
    return edge

def bfs_between((K,V)):
    w = 1 / float(V[WEIGHT])
    edge = []
    for p in V[PATH]:
        edge = edge + bfs_edge(p, K[1])
    return [(e,w) for e in edge]


bfs = pair.map(bfs_init)
print bfs.filter(bfs_left).count()
while (bfs.filter(bfs_left).count() > 0):
    bfs = bfs.flatMap(bfs_map) \
             .reduceByKey(bfs_reduce)

for b in bfs.collect():
    print b

# Step 3
between  = bfs.flatMap(bfs_between) \
              .filter(lambda k: k[0][0] < k[0][1]) \
              .reduceByKey(lambda n1,n2: n1+n2) \
              .collect()
print between