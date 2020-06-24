#include "list.h"

template <class T>
class ListQueue {
    LinkedList<T> list;

public:

    T& front() {
        // Return first element
	return list.front();
	
    }

    void pop() {
        // Remove first element
	list.pop_front();
    }

    bool empty() {
        // Return true if empty, false otherwise
	return list.empty();
    }

    int size() {
        // Return number of elements
	return list.size();
    }

    void push(T& val) {
        // Add a new item at the end of queue
  	list.push_back(val); 
    }

    // You may add other member functions,
    // including constructor and destructor
};
