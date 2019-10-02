import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
lines = f.readlines()

new_lines = []
article_ID = []
shingle_list = []
char_matrix = np.zeros((0,0))
k = 3

# make shingle_list for all lines
for line in lines:
    ID , text = line.split(" ", 1)
    article_ID.append(ID)
    text = re.sub('[^a-zA-Z\s]', '', text) # remove non-world
    text = text.lower()
    new_lines.append(text)
    for i in range(len(text) - k):
        shingle_list.append(text[i:i+3])
    shingle_list = list(set(shingle_list))

print "This is shingle"
print shingle_list

# make Characteristic matrix
num_shingle = len(shingle_list)
char_matrix = np.zeros((num_shingle, num_shingle))

num_line = 0
for line in new_lines:
    for i in range(num_shingle):
        if shingle_list[i] in line:
            char_matrix[i][num_line] = 1
    num_line += 1

print "This is characteristic matrix"
print char_matrix
