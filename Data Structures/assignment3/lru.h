#ifndef LRU_H
#define LRU_H

#include <iostream>
#include "bst.h"
#include "list.h"

struct LRU_Unit {
	int value;
	TreeNode<int, Node<LRU_Unit>*>* tn;

	LRU_Unit(int val = 0, TreeNode<int, Node<LRU_Unit>*>* _tn = nullptr) {
		value = val;
		tn = _tn;
	}
};

class LRU {
	BinarySearchTree<int, Node<LRU_Unit>*> bst;
	LinkedList<LRU_Unit> list;
	int size;
	int misses;

	// You may add additional private member variables and functions

public:
	LRU(int _size) {
		// Constructor
		size = _size;
		misses = 0;
	}

	~LRU() {
		// Destructor
	}

	bool exists(int data) {
		// Return true if data exists in the cache
		// Return false otherwise
		//Look for the data in BST
		if(bst.search(data)!=nullptr)
			return true;
		return false;
	}

	int status() const {
		// Return the number of elements in cache
		return list.size();
	}

	bool touch(int data) {
		// The data is being accessed
		// Return true on hit, false on miss
		// i.e. return true if it existed, and false when it was not
		TreeNode<int, Node<LRU_Unit>*>* t;
		Node<LRU_Unit>* n;
		if(exists(data)) {
			//Finding the tree node has corresponding data, delete its list node and create new list node with same data and push it to the back of the list
			//then change tree node's list pointer to point to new node
			t = bst.search(data);
			list.erase(t->val);
			delete t->val;
			n = list.push_back(data);
			t->val = n;
			n->item.tn = t;
			return true;
		}
		misses+=1;
		 if(status()==size){
				//Remove list node's tree node, update corresponding list node's tree node pointer and pop the list node
				bst.remove(list.front().tn);
				list.front().tn->val->item.tn = list.front().tn;
                        	list.pop_front();
                }
		//Push the new list node to the back of list and insert it to BST, then assign the pointers
		n = list.push_back(data);
		t = bst.insert(data, nullptr);
		t->val = n;
		list.back().tn = t;
		return false;
	}

	int get_misses() {
		// Return the number of cache misses until now
		return misses;
	}

	void print() const {
		bst.print();
		list.print();
	}
};

#endif
