import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
lines = f.readlines()

new_lines = []
article_ID = []
shingle_list = []
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
char_matrix = np.zeros((num_shingle, len(article_ID)))

num_line = 0
for line in new_lines:
    for i in range(num_shingle):
        if shingle_list[i] in line:
            char_matrix[i][num_line] = 1
    num_line += 1

print "This is characteristic matrix"
print char_matrix

# return smallest prime number larger than or equal to n
def prime_num(n):
    while True:
        isprime = True
        for i in range(2, int(n ** 0.5) + 1):
            if (n % i) == 0:
                isprime = False
                break
        if isprime:
            return n
        n += 1

# return random number for hash functions
def hash_gen(c):
    return random.randint(0,c-1), random.randint(0,c-1)

# make signature matrix
#sig_matrix = np.zeros((120, len(article_ID)))