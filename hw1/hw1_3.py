import re
import sys
import random
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
num_article = len(article_ID)
num_shingle = len(shingle_list)
char_matrix = np.zeros((num_shingle, num_article))

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

# make hash matrix whose row is shingle and column is hash value
hash_matrix = np.zeros((num_shingle, 120))
c = prime_num(num_shingle)
for i in range(120):
    a, b = hash_gen(c)
    for j in range(num_shingle):
        hash_matrix[j][i] = (a*j + b) % c

print hash_matrix 

# make signature matrix
sig_matrix = np.full((120, num_article), np.inf)
for i in range(num_shingle):
    for j in range(num_article):
        if char_matrix[i][j] == 1:
            for k in range(120):
                if sig_matrix[k][j] > hash_matrix[i][k]:
                    sig_matrix[k][j] = hash_matrix[i][k]

print sig_matrix

# make band for LSH algorithm and add similar pair
b = 6
r = 20
result = []
for i in range(b):
    band = sig_matrix[:][i*r:(i+1)*r]
    for j in range(num_article):
        for k in range(j+1, num_article):
            for l in range(r):
                if (band[l][j] != band[l][k]):
                    break
            if l == (r-1):
                result.append((j,k))

# make distinct result, and print it
result = list(set(result))
for sim in result:
    print "%s\t%s" % (article_ID[sim[0]], article_ID[sim[1]])
