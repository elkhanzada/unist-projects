# Assignment 1-3: Sorting 10,000,000 integers
In this assignment, you need to implement a function that will sort up to
10,000,000 integers from smallest to largest in C++. Note that there are
numerous sorting algorithms out there. You may try to understand and use
them (but you MUST NOT copy the code directly) or you can devise your own
method. Different from the previous two assignments, for this project, you
should consider up to (not exactly) 10,000,000 integers to sort.
This assignment is very similar to the previous one, except for the number of
data to sort. Therefore, if it is possible to sort within a reasonable time, the
previous sorting method may still be applied. 

We have provided you with ```sort.h``` that contains the following function
declaration.
```c++
void sort(int* numbers, int N)
```
```numbers:``` Numbers you need to sort in increasing order.

```N:``` the number of data to sort.

Implement the function body. It should rearrange the integers so that they are
in increasing order.
Example:
```c++
int nums[] = {9999999, … 10000000 of these integers …,
88};
sort(nums, N); // returns nothing, but nums is now sorted in increasing order.
// nums is now sorted: {0, …, 88, 9999999}
```
We have provided you with main.cpp to give you a better example of how we
will use your function. The code will read numbers from a file and call your sort
function to sort them. 