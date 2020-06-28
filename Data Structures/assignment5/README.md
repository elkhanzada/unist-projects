# Project Assignment 5: B Tree
In binary search trees, each node stores only one item, and the height of the
tree is a factor of log n. Such trees are inefficient when stored in a secondary
storage device (e.g. hard disk) having slow access speed, because nodes that
must be read to search are spread all around the address space. Therefore,
one way to reduce the height of the tree is to define these trees in a specific
range, which is referred to as a B tree.

In this assignment, you will implement a B+ tree, a kind of B tree. In addition,
you will write a report contrasting B+ tree from B tree and about other newly
proposed data structures based on B tree.
## 1. Implementing B+ Tree (80 pts)
You need to implement ```class BPlusTree``` in ```bplustree.h```. The
following is a list of the functions you need to implement. You can add
functions if you want to.
\
In ```class BPlusTree<T>:```
\
```BPlusTree(std::size_t degree)``` Constructor. Make a B+
tree with the given degree
\
```~BPlusTree()``` Destructor.
\
```void search(T data)``` Search a data in the tree
\
```void insert(T data)``` Insert a data in the tree
\
```void remove(T data)``` Remove a data in the tree
\
```int range_search(T start, T end, T* result_data, int arr_length)```
* Return the number of data between ```start``` and ```end```. If the
number of data is more than ```arr_length```, return -1.
* ```arr_length``` is the length of the array ```result_data```.
* After executing this function, ```result_data``` should have all
data which are between ```start``` and ```end```.
* The range is a **closed interval**. This means that start and end
are also in range. It can also be expressed as **[start, end]**.
## 2. Investigate the latest B trees (20 pts)
The B tree is useful in places such as file systems and databases. The B+ tree
we implemented above complements the slow key traversal in the B tree.
Therefore, in this report, we will examine various types of B trees.

Please submit the report in **pdf format** on Blackboard as before. Your report
should be in the length of **3 ~ 5 pages**. Be sure to add **all website address or
article name** you referenced. Note that the reference part is not counted as
your report length. You should write **in your own words** even when you have
included the reference.

Your report must include at least:
* advantages and disadvantages of the B+ tree compared to B tree.
* recently proposed variations of the B tree and its comparison.