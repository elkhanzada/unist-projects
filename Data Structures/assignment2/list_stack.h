#include "list.h"

template <class T>
class ListStack {
    LinkedList<T> list;

public:
    T& top() {
        // Return top element
	list.back();
    }

    void pop() {
        // Remove top element
	list.pop_back();
    }

    bool empty() {
        // Return true if empty, false otherwise
	return list.empty();
    }

    int size() {
        // Return number of elements
	return list.size();
    }

    void push(T& item) {
        // Add a new item at the top
	list.push_back(item);
    }

    // You may add other member functions,
    // including constructor and destructor
};
