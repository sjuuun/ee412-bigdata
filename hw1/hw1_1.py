import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

# split with space, make lower case, remove duplication, and filter non-word
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l)) \
        .map(lambda w: w.lower()) \
        .distinct() \
        .filter(lambda chunk: len(chunk) > 0)

# Take first letter from words, and check it is alphabet
first = words.map(lambda word: (word[0], 1)) \
        .filter(lambda letter: letter[0].isalpha())

# Count words according to first letter
counts = first.reduceByKey(lambda n1, n2: n1 + n2) \
        .sortByKey() \
        .collect()

# Print the result
for index in range(26):
    alpha = chr(ord('a')+index)
    if index < len(counts) and alpha == counts[index][0]:
        print "%s   %d" % (alpha, counts[index][1])
    # If there isn't word starting with alpha, result is 0
    else:
        print "%s   %d" % (alpha, 0)

sc.stop()
