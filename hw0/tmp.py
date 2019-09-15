import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])

# split with space, and filter non-word
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l)) \
        .filter(lambda chunk: len(chunk) > 0)

# Take first letter from words with lower letter, and check it is alphabet
first = words.map(lambda word: (word[0].lower(), 1)) \
        .filter(lambda letter: letter[0].isalpha())

counts = first.reduceByKey(lambda n1, n2: n1 + n2) \
        .sortByKey() \
        .collect()

# counts.saveAsTextFile(sys.argv[2])

print "Test print\n"
for i in range(len(counts)):
    alpha, num = counts[i]
    print "%s   %d" % (alpha, num)

sc.stop()
