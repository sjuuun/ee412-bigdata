import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
lines = f.readlines()

lineList = []

# Split all lines where delimiter is non-word.
# And throw away new-line character.
for line in lines:
    lineList.append(re.split(r'[^\w]+', line)[:-1])

# Add all items in item_List
# Index of item will be hashed value of it.
# Finally, make lineInt which is hashed version of input lines
itemList = []
lineInt = []

for line in lineList:
    tmp = []
    index = 0
    for item in line:
        if item in itemList:
            index = itemList.index(item)
        else:
            itemList.append(item)
            index = len(itemList) - 1
        tmp.append(index)
    lineInt.append(tmp)

# Count all items.
numItems = len(itemList)
frequency = [0] * numItems

for line in lineInt:
    for item in line:
        frequency[item] += 1

# Filter with threshold
# Append frequent items in freqList with hashed value.
threshold = 200
freqList = []
for i in range(numItems):
    if frequency[i] >= threshold:
        freqList.append(i)

# Print number of frequent items.
numFreq = len(freqList)
print numFreq

# Make triangular matrix to count frequency of pairs.
# And count all pairs
freqPair = np.zeros((numFreq, numFreq))

for line in lineInt:
    for i in range(len(line)):
        for j in range(i+1, len(line)):
            if (line[i] in freqList) and (line[j] in freqList):
                ind1 = freqList.index(line[i])
                ind2 = freqList.index(line[j])
                if ind1 < ind2:
                    freqPair[ind1][ind2] = freqPair[ind1][ind2] + 1
                else:
                    freqPair[ind2][ind1] = freqPair[ind2][ind1] + 1

# Count number of frequent pairs with threshold.
numPair = 0
for i in range(numFreq):
    for j in range(i+1, numFreq):
	if (freqPair[i][j] >= threshold):
	    numPair += 1
print numPair

# Print top-10 most frequent pairs
for i in range(10):
    ind1, ind2 = np.unravel_index(freqPair.argmax(), freqPair.shape)
    count = freqPair[ind1][ind2]
    freqPair[ind1][ind2] = 0
    item1 = itemList[freqList[ind1]]
    item2 = itemList[freqList[ind2]]
    
    print "%s\t%s\t%d" % (item1, item2, count)
