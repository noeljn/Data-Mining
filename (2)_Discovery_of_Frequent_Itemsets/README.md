# Introduction

The problem of discovering association rules between itemsets in a sales transaction database (a set of baskets) includes the following two sub-problems [R. Agrawal and R. Srikant, VLDB '94](Links to an external site.):

1. Finding frequent itemsets with support at least s;
2. Generating association rules with confidence at least c from the itemsets found in the first step.

Remind that an association rule is an implication X → Y, where X and Y are itemsets such that X∩Y=∅. Support of rule X → Y is the number of transactions that contain X⋃Y. Confidence of rule X → Y is the fraction of transactions containing X⋃Y in all transactions that contain X.

## Task

You are to solve the first sub-problem: to implement the A-Priori algorithm for finding frequent itemsets with support at least s in a dataset of sales transactions. Remind that support of an itemset is the number of transactions containing the itemset. To test and evaluate your implementation, write a program that uses your A-Priori algorithm implementation to discover frequent itemsets with support at least s in a given dataset of sales transactions.

The implementation can be done using any big data processing framework, such as Apache Spark, Apache Flink, or no framework, e.g., in Java, Python, etc.

### The optional task for an extra bonus

Solve the second sub-problem, i.e., develop and implement an algorithm for generating association rules between frequent itemsets discovered using the A-Priori algorithm in a dataset of sales transactions. The rules must have the support of at least s and confidence of at least c, where s and c are given as input parameters.

## Datasets

As a sale transaction dataset, you can use this [https://canvas.kth.se/courses/42990/files/6945385/download?wrap=1](Download dataset), which includes generated transactions (baskets) of hashed items – you use any browser, e.g., Google Chrome, or a text editor, e.g., WordPad, to view the file under Windows.

You can also use any other transaction datasets as an input dataset found on the Web.
