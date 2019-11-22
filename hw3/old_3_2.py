import sys
from pyspark import SparkConf, SparkContext

def author_group(group):
    result = []
    for i in range(len(group)):
        result.append((group[i], group[:i] + group[(i+1):]))
    return result

# Define for BFS
DONE = 0
DIST = 1
WEIGHT = 2
PATH = 3

def bfs_init(point):
    return ((point, point), [0,0,1,[[]]] )

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


if __name__=="__main__":
    # Get imput
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(sys.argv[1])

    # Remove header from .csv file
    header = lines.take(1)[0]
    # pairs: RDD of [list of user_id]
    pairs = lines.filter(lambda line: line != header) \
                .map(lambda line: list(map(int, line.split(','))) ) \
                .map(lambda pair: (pair[1], [pair[2]])) \
                .reduceByKey(lambda n1, n2: n1+n2) \
                .map(lambda group: group[1])

    adjPoint = pairs.flatMap(author_group) \
                    .reduceByKey(lambda n1, n2 : list(set(n1+n2))) \
                    .collectAsMap()

    bfs = pairs.flatMap(lambda group: group) \
                .distinct() \
                .map(bfs_init)
    
    c = 0
    graph = []
    while (not bfs.isEmpty()): #bfs.filter(bfs_left).count() > 0):
        bfs = bfs.flatMap(bfs_map) \
                .reduceByKey(bfs_reduce)
        graph += bfs.filter(lambda d: d[1][DONE]).collect()
        bfs = bfs.filter(lambda d: not d[1][DONE])
        c += 1
        print "HELLO IT'S COUNT: %d" % c
    print bfs.collect()
    print graph

    between  = sc.parallelize(graph) \
                 .filter(lambda p: p[1][DIST] != 0) \
                 .flatMap(bfs_between) \
                 .filter(lambda k: k[0][0] < k[0][1]) \
                 .reduceByKey(lambda n1,n2: n1+n2) \
                 .collect()
    between.sort(key = lambda x: -x[1])
    print between