import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
line = f.readline()

article_ID = []
shingle_list = []
char_matrix = np.zeros((0,0))
k = 3

def find_shingle_index(s):
    if s in shingle_list:
        return shingle_list.index(s)
    else:
        return -1

while(line != ""):
    ID , text = line.split(" ", 1)
    article_ID.append(ID)
    text = re.sub('[^a-zA-Z\s]', '', text)
    column = np.zeros((len(shingle_list), 1))
    col_size = char_matrix.shape[1]

    for i in range(len(text)-k): #len(text)-k
        shingle = text[i:i+3]
        index = find_shingle_index(shingle)
        if (index >= 0):
            shingle_list[index] = 1
        else:
            shingle_list.append(shingle)
            char_matrix = np.vstack([char_matrix, np.zeros(col_size)])
            column = np.vstack([column, [1]])
    char_matrix = np.append(char_matrix, column, axis=1)

    line = f.readline()

print article_ID
print shingle_list
print char_matrix


