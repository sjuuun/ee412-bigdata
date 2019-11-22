import sys
from pyspark import SparkConf, SparkContext

def author_group(group):
    result = []
    for i in range(len(group)):
        result.append((group[i], group[:i] + group[(i+1):]))
    return result

def GN_per_root(root):
    # Node information: (distance, weight)
    node = {root:(0,1)}
    # Dictionary: parents of node(used in step3)
    parent = {}
    after = [root]
    cur = []
    # Step 1 & 2: label depth and node weights
    while(len(after) != 0):
        cur = after
        after = []
        # Temporal node information
        tmpNode = {}
        for c in cur:
            tmp = [p for p in adjPoint[c] if not(p in node)]
            for t in tmp:
                # Update node
                if tmpNode.get(t):
                    tmpNode[t] = (tmpNode[t][0], tmpNode[t][1] + node[c][1])
                else:
                    tmpNode[t] = (node[c][0] + 1, node[c][1])

                # Update parent
                if parent.get(t):
                    parent[t].add(c)
                else:
                    parent[t] = set([c])
            
            after += tmp

        node.update(tmpNode)
        after = list(set(after))

    # Step 3: compute edge weight
    allnode = list(node)
    allnode.sort(key = lambda n: -node[n][0]) # start from leaf
    # Dictionary for node and weighted-value: (node, value)
    nodeWeight = {}
    result = []
    for a in allnode[:-1]:
        if nodeWeight.get(a):
            my = nodeWeight[a] + 1
        else: # leaf
            my = 1
        for p in list(parent[a]):
            parentWeight = (my*node[p][1]) / float(node[a][1])
            # Update edge weight
            if p < a:
                result.append(((p, a), parentWeight))
            else:
                result.append(((a, p), parentWeight))
            
            # Update parent's node weight
            if nodeWeight.get(p):
                nodeWeight[p] += parentWeight
            else:
                nodeWeight[p] = parentWeight

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
                .map(lambda group: group[1]) \
                .filter(lambda k: len(k) > 1)

    adjPoint = pairs.flatMap(author_group) \
                    .reduceByKey(lambda n1, n2 : list(set(n1+n2))) \
                    .collectAsMap()
    
    #gn = pairs.flatMap(lambda group: group) \
    gn = sc.parallelize(adjPoint) \
                .flatMap(GN_per_root) \
                .reduceByKey(lambda n1, n2: n1+n2) \
                .collect()
                                #.distinct() \

    gn.sort(key = lambda x: -x[1])
    for g in gn[:10]:
        print ("%d\t%d\t%.5f" % (g[0][0], g[0][1], g[1]/2))