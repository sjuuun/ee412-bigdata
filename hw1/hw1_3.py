import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
line = f.readline()

article_ID = []
shingle_list = []

for i in range(1):
    ID , text = line.split(" ", 1)
    print "This is ID"
    print ID
    print "This is text"
    print text



