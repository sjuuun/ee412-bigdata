import re
import sys

f = open(sys.argv[1], 'r')
lines = f.readlines()
divide = []

for line in lines:
    divide.append(re.split(' ', line))
print divide