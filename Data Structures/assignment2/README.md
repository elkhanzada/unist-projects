# Assignment 2: FIFO, LIFO Policy
In computers, the notion of cache is very important. (You will learn about this in
other courses in CSE.) For now, let us just understand what is described below,
and use this knowledge for our programming assignments.
Consider a storage device that can keep N items, where each of these items are
unique and are of the same unit, which we will call a block. It turns out that not
all these items are used evenly, but there are some “hot” items, which are used
often, and some may be “cold”, that is, hardly used. Essentially, the access of
these items has particular characteristics, depending on various many factors.
Now, storage devices are generally very slow. So, we would like to keep these
items in memory, which is much faster than storage. However, as memory is
generally much smaller than storage, we can keep only some of the items, say
k, where k << N. This small memory is called a cache. Since we can only keep a
small number of items, k, we want to keep the “hot” items, that is, those that
will be used often. Thus, as an item is requested to be used by the user (an
application), if it is found in the cache it will be serviced (to the user) from the
cache. However, if it is not found in the cache, it is brought from storage and
placed in the cache, and then serviced to the user. Now, the cache may already
be full (that is, already holding k items). Then, one of the k items must first be
removed to make space, so that the new item can be placed there. Which of the
items to remove in such a case is an important policy issue, which we will call
the replacement policy (or algorithm). Judiciously, replacement algorithms can
have a vast effect on the performance of the system.
In this assignment (and subsequent ones throughout the semester), we are
going to implement (in C++) a couple of replacement algorithms. In particular,
they are the FIFO and LIFO policies. As you know, FIFO is short for "First In First
Out" and LIFO is short for "Last In First Out". Thus, FIFO replacement choice to
replace is the first one among the cached items. In contrast, LIFO chooses the
last one that came into the cache. You are to implement these policies using
data structures that you learned so far in class (that is, array, list, linked lists,
stacks, queues). In this assignment, you will need to implement each policy with
an array and list respectively, then compare their performance.
## 1. Implementing double-linked list (30 pts)
First, you need to implement Class ```LinkedList``` in ```list.h```. Class Node is
already implemented for you. Here is a description of functions you need to
implement.

Class ```List```
\
```LinkedList():``` constructor
\
```~LinkedList()``` destructor
\
```T& front()``` access the first element
\
```T& back()``` access the last element
\
```bool empty()``` check whether the container is empty
\
```int size()``` return the number of elements
\
```void insert(Node<T>* node_before, type val)``` create a
node with the element and insert it after ```node_before```
\
```void erase(Node<T>* target)``` erase an element
\
```void push_front(T val)``` add an element at the front
\
```void pop_front()``` erase the first element
\
```void push_back(T val)``` add an element at the back
\
```void pop_back()``` erase the last element
\
```Node<T>* find(T val)``` find an element of item val
## 2. Implementing FIFO policy with array and list (30 pts)
You need to implement classes ```ListQueue``` and ```ArrayQueue``` in
```list_queue.h``` and ```array_queue.h```, respectively. In ```ListQueue```, you
need to utilize class ```List``` you implemented earlier. ```ArrayQueue``` class
basically does the same thing, but utilizes an array as its base data structure
instead of a list. Here is a description of functions you need to implement for
both.

Classes ```ArrayQueue``` and ```ListQueue:```
\
Constructor ```ArrayQueue()/ListQueue()```
\
Destructor ```~ArrayQueue()/~ListQueue()```
\
```void push(const type& item)``` push an element to the
container
\
```type& front()``` return the first element in the container
\
```void pop()``` delete the first element in the container
\
```bool empty()``` check whether the container is empty
\
```int size()``` return the number of elements currently stored
## 3. Implementing LIFO policy with array and list (30 pts)
You need to implement classes ```ListStack``` and ```ArrayStack``` in
```list_stack.h``` and ```array_stack.h```, respectively. In ```ListStack```, you
need to utilize class ```List``` you implemented earlier. ```ArrayStack``` class
basically does the same thing, but utilizes an array as its base data structure
instead of a list. Here is a description of functions you need to implement for
both.

Classes ```ListStack``` and ```ArrayStack:```
\
Constructor ```ListStack()/ArrayStack()```
\
Destructor ```~ListStack()/~ArrayStack()```
\
```void push(const type& item)``` push an element to the
container
\
```type& top()``` return the top element in the container
\
```void pop()``` delete the element at the top
\
```bool empty()``` return true if the container is empty
\
```int size()``` return the number of elements currently stored
## 4. Analysis of array and list implementation (10 pts)
You need to submit report on the performance analysis (and/or measurement)
of array and list implementations. Please submit the report in pdf format on
Blackboard as before.
Your report must include at least the following:

* Basic description of your implementation.
\
* Difference between two implementations of LIFO and FIFO
\
  * e.g. Array implementation is slower when inserting, because …
\
  * show performance measurement number if applicable
\

Your report should be no longer than 3 pages.