# ee412-bigdata
Foundation of Big Data Analytics

## Homework 0
1. Word count example

In this example, you have to count the number of words that start with each letter.
```
spark-submit hw0.py pg100.txt
```

## Homework 1
1. Find potential friends in a social network using Spark
 
 You have to find pairs of users who are not friends with each other, but have many common friends.  
 soc-LiveJournal1Adj.txt have data of user and his or her friends.  
 Show pair and their common friends.  

```
spark-submit hw1_1.py soc-LiveJournal1Adj.txt
```

2. Find frequent itemsets using the A-Priori algotirhm

 Find frequent items and item pairs.
 
```
python hw1_2.py browsing.txt
```

3. Find similar documents using minhash-based LSH

 Implement minhash-based LSH algorithm to find articles that have high Jaccard similarities.

```
python hw1_3.py articles.txt
```

## Homework 2
1. Implement K-Means algorithm using Spark

 After clustering, print average diameter of the given number of cluster.

 ```
 spark-submit hw2_1.py kmeans.txt k_value
 ```

2. Implement collaborative filtering

 Implement user-based and item-based collaborative filtering and run it on a real movie dataset.
 
  ```
  python hw2_3b.py ratings.txt
  ```
 
 3. Movie recommendation challenge
 
  Similar to the Netflix Challenge.
 
  ```
  python hw2_3c.py rating_test.txt
  ```
 
 ## Homework 3
 1. Implement the PageRank algorithm using Spark
 
  The graph is randomly generated and has 1000 nodes and about 8000 edges with no dead ends.  
  For each row, the left page id represents the source and the right id represents the destination.
  
  ```
  spark-submit hw3_1_p2.py graph.txt
  ```
 
 2. Implement Girvan-Newman algorithm using Spark
 
  Dataset consists of Input, paper_id, and user_id.  
  We want to cluster authors whose papers ard published. Show top-10 betweeness.
  
  ```
  spark-submit hw3_2_p2.py paper_authors.csv
  ```

3. Implement the gradient descent SVM algorithm using Python

 Use 10-fold cross validation.
 
 ```
 python hw3_3_p2.py features.txt labels.txt
 ```

## Homework 4
1. Implement a fully-connected network to distinguish digits using Python

 Using MNIST dataset, implement fully-connected network
 
 ```
 python hw4_1_p2.py training.csv testing.csv
 ```

2. Implement DGIM algorithm

 Implement DGIM algorithm using the stream.
 
 ```
 python hw4_2_p2.py stream.txt k1 k2 k3 ... km
 ```
