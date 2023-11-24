# Introduction

The following three papers present streaming graph processing methods and corresponding algorithms that make use of the stream mining algorithms presented in the course (Lecture 5, Lecture 6, and Chapter 4 of the textbook Mining of Massive Datasets), namely, the reservoir sampling (Lecture 5) and the Flajolet-Martin algorithm to estimate the number of distinct elements in a stream (Lecture 6). The graph algorithms presented in the first two papers use the reservoir sampling technique; the graph algorithm in the third paper uses the Flajolet-Martin algorithm (HyperLogLog counters).

- M. Jha, C. Seshadhri, and A. Pinar, A Space-Efficient Streaming Algorithm for Estimating Transitivity and Triangle Counts Using the Birthday Paradox, ACM TKDD, 9-3, 2015.
- L. De Stefani, A. Epasto, M. Riondato, and E. Upfal, TRIÈST: Counting Local and Global Triangles in Fully-Dynamic Streams with Fixed Memory Size, KDD'16.
- P. Boldi and S. Vigna, In-Core Computation of Geometric Centralities with HyperBall: A Hundred Billion Nodes and Beyond, ICDMW'13.

## Task

You are to study and implement a streaming graph processing algorithm described in one of the above papers of your choice. To accomplish your task, you are to perform the following two steps:

1. Implement the reservoir sampling or the Flajolet-Martin algorithm used in the graph algorithm presented in the paper you have selected.
2. Implement the streaming graph algorithm presented in the paper that uses the algorithm implemented in the first step.

To ensure that your implementation is correct, you are to test your implementation with some of the publicly available graph datasets (find a link below) and present your test results in a report.

Implementation can be done using any data processing framework that includes support for stream (streaming graph) processing, such as Apache Spark, Apache Flink, or no framework, e.g., in Java, Python, or another language of your choice.

## The optional task for an extra bonus

In your report, answer the following questions:

1. What were the challenges you faced when implementing the algorithm?
2. Can the algorithm be easily parallelized? If yes, how? If not, why? Explain.
3. Does the algorithm work for unbounded graph streams? Explain.
4. Does the algorithm support edge deletions? If not, what modification would it need? Explain.

## Datasets

Graph datasets can be found by following this [link](Links to an external site.) (see, in particular, datasets under "Web graphs [Links to an external site.])." Note that information about each dataset (you can see it when you click on a dataset name) includes several metrics, e.g., Triangle Count, that you can use to verify your results.
