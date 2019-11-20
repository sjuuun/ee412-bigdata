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
'''
class BFS:
    def __init__ (self, point):
        self.src = point
        self.dst = point
        self.distance = 0
        self.weight = 1
        self.path = []
        self.adjacent = adjPoint[point]
    def print_bfs(self):
        print "src: %d, dst: %d, dis: %d, weight: %d" % (self.src, self.dst, self.distance, self.weight)
        print self.path
        print self.adjacent
    def map(self):
        return ((self.src, self.dst), self)
'''
DIST = 0
WEIGHT = 1
PATH = 2
ADJACENT = 3

def bfs_init(point):
    return ((point, point), [0,1,[],adjPoint[point]])

def bfs_adj(path, adj):
    return [p for p in adj if not(p in path)]

def bfs_next(data, target):
    (src, dst), [dis, weight, path, adj] = data
    assert (target in adj)
    dis += 1
    path = path + [dst]
    adj = bfs_adj(path, adjPoint[target])
    return ((src, target), [dis, weight, path, adj])

def bfs_map(data):
    if len(data[1][ADJACENT]) == 0:
        return [data]
    else:
        result = [bfs_next(data, p) for p in data[1][ADJACENT]]
        data[1][ADJACENT] = []
        return [data] + result

start = pair.keys().distinct() \
            .map(lambda k: bfs_init(k))


bfs = start.flatMap(bfs_map)
have = bfs.map(lambda d: d[0]).distinct().collect()
print have
#for s in start.collect():
#    print s
for b in bfs.collect():
    print b
