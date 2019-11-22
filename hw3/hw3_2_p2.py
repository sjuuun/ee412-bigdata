import sys
from pyspark import SparkConf, SparkContext

def author_group(group):
    result = []
    for i in range(len(group)):
        result.append((group[i], group[:i] + group[(i+1):]))
    return result

def update_hitPoint(hitPoint, group):
    for g in group:
        src, hit = g
        hitPoint[src] += [h[0] for h in hit]

def GN_per_root(root):
    node = {root:(0,1)}
    parent = {}
    after = [root]
    cur = []
    # Step 1 & 2: label depth and node weights
    count = 0
    while(len(after) != 0):
    #for _ in range(4):
        cur = after
        after = []
        tmpNode = {}
        for c in cur:
            tmp = [p for p in adjPoint[c] if not(p in node)]
            for t in tmp:
                # Update node
                if t in tmpNode:
                    tmpNode[t] = (tmpNode[t][0], tmpNode[t][1] + 1)
                else:
                    tmpNode[t] = (node[c][0] + 1, node[c][1])

                # Update parent
                if t in parent:
                    parent[t].add(c)
                else:
                    parent[t] = set([c])
            after += tmp
        node.update(tmpNode)
        #print cur
        #print after
        #print parent
        #print node
        #cur = list(set(after))
        after = list(set(after))
        #print "HELLO IT'S COUNT: %d" % count
        count += 1
    #print len(node)

    # Step 3: compute edge weight
    allnode = list(node)
    allnode.sort(key = lambda n: -node[n][0])
    nodeWeight = {}
    result = []
    for a in allnode[:-1]:
        if a in nodeWeight:
            my = nodeWeight[a] + 1
        else:
            my = 1
        for p in list(parent[a]):
            parentWeight = (my*node[p][1]) / float(node[a][1])
            result.append(((p, a), parentWeight))
            if p in nodeWeight:
                nodeWeight[p] += parentWeight
            else:
                nodeWeight[p] = parentWeight
    #print result
    return result

if __name__=="__main__":
    # Get imput
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(sys.argv[1])

    # Remove header from .csv file
    header = lines.take(1)[0]
    # pairs: RDD of [list of co-authors]
    pairs = lines.filter(lambda line: line != header) \
                .map(lambda line: list(map(int, line.split(','))) ) \
                .map(lambda pair: (pair[1], [pair[2]])) \
                .reduceByKey(lambda n1, n2: n1+n2) \
                .map(lambda group: group[1])

    adjPoint = pairs.flatMap(author_group) \
                    .reduceByKey(lambda n1, n2 : list(set(n1+n2))) \
                    .collectAsMap()
    
    '''
    tmp = pairs.flatMap(lambda group: group) \
                .distinct().take(1) # \
                #.map(bfs_init)
    print tmp
    '''
    
    gn = pairs.flatMap(lambda group: group) \
                .distinct() \
                .flatMap(GN_per_root) \
                .filter(lambda k: k[0][0] < k[0][1]) \
                .reduceByKey(lambda n1, n2: n1+n2) \
                .collect()
    
    gn.sort(key = lambda x: -x[1])
    print gn[:10]
    for g in gn[:10]:
        print ("%d\t%d\t%.5f" % (g[0][0], g[0][1], g[1]))
    #gn = sc.parallelize([94]).map(GN_per_root)
    #GN_per_root(5)
    print "DONE"
    #print len(gn.filter(lambda k: k[0][0] < k[0][1]).reduceByKey(lambda n1, n2: n1+n2).collect())
    #print len(gn.collect())

    #bfs = sc.parallelize(tmp).map(bfs_init)

    '''
    c = 0
    while (len(level[-1]) != 0):
    #for i in range(4):
        tmp = sc.parallelize(level[-1]) \
                .flatMap(bfs_map) \
                .reduceByKey(lambda n1, n2: n1+n2) \
                .map(lambda data: (data[0][0], (data[0][1], data[1])))
        level.append(tmp.collect())
        hit = tmp.groupByKey().mapValues(list).collect()
        #print hit
        update_hitPoint(hitPoint, hit)
        print "HELLO IT'S COUNT: %d" % c
        c += 1
    #print hitPoint
    #print level'''
