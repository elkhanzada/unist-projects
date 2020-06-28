# Assignment 1: Sorting 100 integers

In this assignment, you need to implement a function that will sort 100
integers from smallest to largest in C++. Note that there are numerous sorting
algorithms out there. You may try to understand and use them (but you MUST
NOT copy the code directly) or you can devise your own method. Remember,
for this project, you need only consider the case where you have exactly 100
integers to sort.
We have provided you with ```sort.h``` that contains the following function
declaration.
```c++
void sort(int* numbers)
```
``` numbers ``` Numbers you need to sort in increasing order.

Implement the function body. It should rearrange the integers so that they are
in increasing order.

Example:
```c++
int nums[] = {90, … 100 of these integers …, 88};
sort(nums); // returns nothing, but nums is now sorted in increasing order. 
// nums is now sorted: {27, …, 88, 90}
```
We have provided you with main.cpp to give you a better example of how
we will use your function. The code will read numbers from a file and call your
sort function to sort them.