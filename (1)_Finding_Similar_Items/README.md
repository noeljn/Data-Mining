# ID2222

# Homework 1: Finding Similar Items: Textually Similar Documents 

The homework can be done in a group of 2 students.

## Task

You are to implement the stages of finding textually similar documents based on Jaccard similarity using the shingling, minhashing, and locality-sensitive hashing (LSH) techniques and corresponding algorithms. The implementation can be done using any big data processing framework, such as Apache Spark, Apache Flink, or no framework, e.g., in Java, Python, etc. To test and evaluate your implementation, write a program that uses your implementation to find similar documents in a corpus of 5-10 or more documents, such as web pages or emails.

The stages should be implemented as a collection of classes, modules, functions, or procedures depending on the framework and the language of your choice. Below, we describe sample classes implementing different stages of finding textually similar documents. You do not have to develop the exact same classes and data types described below. Feel free to use data structures that suit you best.

- A class `Shingling` that constructs k–shingles of a given length k (e.g., 10) from a given document, computes a hash value for each unique shingle and represents the document in the form of an ordered set of its hashed k-shingles.
- A class `CompareSets` computes the Jaccard similarity of two sets of integers – two sets of hashed shingles.
- A class `MinHashing` that builds a minHash signature (in the form of a vector or a set) of a given length n from a given set of integers (a set of hashed shingles).
- A class `CompareSignatures` estimates the similarity of two integer vectors – minhash signatures – as a fraction of components in which they agree.
- (Optional task for extra 2 bonus points) A class `LSH` that implements the LSH technique: given a collection of minhash signatures (integer vectors) and a similarity threshold t, the LSH class (using banding and hashing) finds candidate pairs of signatures agreeing on at least a fraction t of their components.

To test and evaluate your implementation's scalability (the execution time versus the size of the input dataset), write a program that uses your classes to find similar documents in a corpus of 5-10 documents. Choose a similarity threshold s (e.g., 0.8) that states that two documents are similar if the Jaccard similarity of their shingle sets is at least s.

## Datasets

For documents, see the datasets in the [UC Irvine Machine Learning Repository](Links to an external site.), or find other documents such as web pages or emails. To find more datasets, follow [this link](Links to an external site.).

## Readings

- Lecture "Finding Similar Items"
- Chapter 3 in *Mining of Massive Datasets*, by Jure Leskovec, Anand Rajaraman, and Jeffrey D. Ullman, 3rd edition, Cambridge University Press, 2020 ([http://www.mmds.org/](Links to an external site.))

## Submission, Presentation, and Demonstration

To submit your homework, you upload your solution in a zip file to Canvas. Canvas records the submission time. Your homework solution must include:

- Source code if required (with comments)
- Makefile or scripts to build and run
- Report (in PDF) with a short description of your solution, instructions on how to build and run, command-line parameters, if any (including default values), and results, e.g., plots or screenshots.

Within a week after the homework deadline, you present and demonstrate your homework on your laptop to a course instructor. A Doodle pool will be provided to book a time slot for the presentation.

## Grading and Bonus Policy

The grade for homework is pass/fail. If you submit your solution on time and it is accepted, you will get up to 3 bonus points on the ID2222 exam. Some homework assignments include an optional task for an extra bonus. The total bonus can be reduced for minor errors and inefficiency of your solution. A bonus will not be given if you miss the deadline.
