#ifndef LIST_H
#define LIST_H

template <class T>
class Node {
    /*
     * This is a wrapper around 'item', the element we want to store.
     *
     * Template is used to make it work regardless of what type 'T' is.
     * Refer to http://www.cplusplus.com/doc/oldtutorial/templates/ for more info.
     */
public:
    Node* prev;
    Node* next;
    T item;

    Node(T val = T()) {
        prev = nullptr;
        next = nullptr;
        item = val;
    }
};

// Part 1: Implement a doubly linked list.
template <class T>
class LinkedList {
    // Dummy nodes
    Node<T>* head;
    Node<T>* tail;
    int length;

    // You may add member variables you need.
    void init(){
	length=0;
        head = new Node<T>;
        tail = new Node<T>;

        head->prev = nullptr;
        head->next = tail;

        tail->prev = head;
        tail->next = nullptr;
	
    }

public:
    LinkedList() {
        // Constructor.
	init();

        // Initialize your variables if you added them.
    }

    ~LinkedList() {
        // Destructor.
        clear();
        delete head;
        delete tail;

        // Release yours if you added them.
    }

    // Implement member functions below.
    // Remember: member functions can call each other.

    int size() {
        // Return the number of elements in list.
	return length;
    }

    bool empty() {
	if(head->next==tail){
		return true;
	}
	return false;
        // Return true if no elements are in list and false otherwise.
    }

    T& front() {
	return head->next->item;
	
        // Return the front (first) element.
        // Note the return type.
        // It is REFERENCE (not value) of the ITEM (not Node).
    }

    T& back() {
	return tail->prev->item;

        // Return the back (last) element.
        // Same note as in front().
    }

    void insert(Node<T>* node_before, T val) {
        // Create a node with val. Insert it after node_before.
        // i.e. node_before -> new node -> node_before->next
	Node<T>* t = new Node<T>(val);
 	if(node_before==tail) return;
	t->next = node_before->next;
	t->prev = node_before;
	node_before->next->prev=t;
	node_before->next = t;
	length+=1;
    }

    void erase(Node<T>* target) {
        // Remove target node from the list.
	Node<T>* prevNode=target->prev;
	prevNode->next = target->next;
	target->next->prev=prevNode;
	delete target;
	length-=1;
    }

    void push_front(T val) {
        // Create a node with val. Add it to the front of the list.
	insert(head, val);
    }

    void pop_front() {
        // Remove the front node.
	erase(head->next);
    }

    void push_back(T val) {
        // Create a node with val. Add it to the back of the list.
	insert(tail->prev, val);
    }

    void pop_back() {
        // Remove the back node.
	erase(tail->prev);
    }

    void clear() {
        // Remove all nodes in list.
	Node<T>* t = head;
	if(empty()) return;
	while(head){
		head= head->next;
		delete t;
		t = head;
			
	}
	init();
	
    }

    Node<T>* find(T val) {
        // Return the pointer of first node with the item val.
	Node<T>* t = head->next;
	while(t!=0){
		if(t->item==val) return t;
		t = t ->next;
	}
	return nullptr;
    }

    // You may add other member functions.
};

#endif
