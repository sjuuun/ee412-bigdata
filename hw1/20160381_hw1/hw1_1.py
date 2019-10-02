import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

# Split all lines where delimiter is tab and comma
# If someone who has not friend is filtered 
split = lines.map(lambda l: re.split(r'\t|,', l)) \
        .filter(lambda l: l[-1] != '')

# making pair of two people from line.
# Key is tuple of two people. (ascending order)
# If both are friend value is 0, otherwise value is 1.
# The value is useful when filtering pair of friend.
def make_pair(x):
    who = x[0]
    friends = x[1:]
    result = []
    for i in range(len(friends)):
        result.append(((who, friends[i]), 0))               # pair of real friends
        for j in range(i+1, len(friends)):
            result.append(((friends[i], friends[j]), 1))    # pair of not friends
    return result

# This is reduce function. It counts number of common friends.
# Here, we use value 0.
# If one of value is 0, keep it to distinguish real friends.
def count_common(n1, n2):
    if n1*n2 == 0:
        return 0
    else:
        return n1 + n2

# Make pair, count common friend with above functions.
# If a pair is real friend(value is 0), filter it.
pairs = split.flatMap(make_pair) \
        .reduceByKey(count_common) \
        .filter(lambda p: p[1] != 0)

# Take top 10 pairs with their counts in descending order.
final = pairs.takeOrdered(10, key = lambda x: -x[1])

# Sort final list with their counts first.
# Then, sort with their userID if there are ties in counts.
final.sort(key = lambda pair: (-pair[1], pair[0]))

# Print the final result
for i in final:
	print "%s\t%s\t%d" % (i[0][0], i[0][1], i[1])

sc.stop()
