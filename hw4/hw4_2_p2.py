import sys

# If 3 buckets have same size, merge it.
def merge_bucket(bucket):
    if len(bucket) < 3:
        return True

    tmp = []
    while (len(bucket) >= 3) and (bucket[-3][1] == bucket[-2][1] == bucket[-1][1]):
        tmp.append(bucket.pop())
        a = bucket.pop()
        b = bucket.pop()
        assert(a[0] > b[0])
        bucket.append((a[0], a[1] + 1))
    while (len(tmp) > 0):
        bucket.append(tmp.pop())
    return True


if __name__ == "__main__":
    #sys.stdin = open(sys.argv[1], 'r')
    f = open(sys.argv[1], 'r')
    k_list = []
    for i in range(2, len(sys.argv)):
        k_list.append(int(sys.argv[i]))

    stream = f.readlines()
    bucket = []
    timestamp = 0

    for s in stream:
        timestamp += 1
        a = int(s)

        # If a is 0, pass
        if a == 0:
            continue

        # If a is 1, add bucket whose size is 1
        bucket.append((timestamp, 0))
        merge_bucket(bucket)

    print bucket
    print timestamp

    # Predict with k
    print k_list
    for k in k_list:
        limit = timestamp - k
        candidate = [x[1] for x in bucket if x[0] > limit]
        print candidate
        if len(candidate) > 0:
            candidate[0] -= 1
            result = sum(2**c for c in candidate)
        else:
            result = 0
        print (result)