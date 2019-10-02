import numpy as np
import random

test = np.zeros((2,1), int)

test[1] = 3
test = np.vstack([test, [0]])
print test

col = test.shape[1]
print col

hello = np.zeros((0,0))
print hello

hellw = np.zeros((0,1))
print hellw

lis = [1,2,3,4,5,5,1]
print list(set(lis))

print int(10 ** 0.5)

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

print "prime"
print prime_num(19)

def hash_gen(x):
    return random.randint(0,x-1), random.randint(0,x-1)

a, b = hash_gen(5)
print a
print b

num_shingle = 10
# make signature matrix
hash_matrix = np.zeros((num_shingle, 12))
c = prime_num(num_shingle)
for i in range(12):
    a, b = hash_gen(c)
    for j in range(num_shingle):
        hash_matrix[j][i] = (a*j + b) % c

print hash_matrix

print np.inf < 3

r = 0
for l in range(3):
    if l == 1:
        break
    r += l
print l
print r
print "%d\t%d" % (l, r)

tri = np.full((3,3), np.inf)
tri = np.triu(tri, 1)
print tri