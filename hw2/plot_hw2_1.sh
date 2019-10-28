#!/bin/bash

echo "Print the average diameter of the given number of cluster"
echo "Print the average diameter" > output.txt

declare -i k=1
for (( i=0; i<4; i++ ))
do
	echo "${i}"
	echo "k is ${k}"
	echo "k is ${k}" >> output.txt
	spark-submit hw2_1.py kmeans.txt ${k} | grep -v 2019 >> output.txt
	echo "Done"
	echo "Done" >> output.txt
	k=k*2
done
