import sys

def merge_bucket(bucket):
    tmp = [bucket.pop()]
    while (tmp[-1][1] != bucket[-1][1]):
        a = tmp.pop()
        b = bucket.pop()
        merged = (a[0], a[1] + b[1])
        tmp.append(merged)
    while (len(tmp) > 0):
        bucket.append(tmp.pop())

#sys.stdin = open(sys.argv[1], 'r')
f = open(sys.argv[1], 'r')
k = []
for i in range(2, len(sys.argv)):
    k.append(int(sys.argv[i]))
print k

stream = f.readlines()
bucket = []
timestamp = 0

for s in stream:
    timestamp += 1
    a = int(s)

    if a == 0:
        continue

    new_block = [timestamp, 1, 1]


print timestamp