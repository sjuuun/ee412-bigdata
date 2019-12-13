#!/bin/bash

echo "Repeat HW4_1" > output.txt

ITER=10
for ((i = 0; i < ITER; i++))
do
	echo "${i}th time" >> output.txt
	python hw4_1_p2.py training.csv testing.csv >> output.txt
done
