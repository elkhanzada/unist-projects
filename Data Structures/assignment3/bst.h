#ifndef BST_H
#define BST_H

#include <iostream>

template <typename keyT, typename valT>
struct TreeNode {
	keyT key;
	valT val;
	TreeNode* parent;
	TreeNode* left;
	TreeNode* right;

	TreeNode(keyT _key = keyT(), valT _val = valT(), TreeNode* _parent = nullptr) {
		key = _key;
		val = _val;
		parent = _parent;
		left = nullptr;
		right = nullptr;
	}
};

template <typename keyT, typename valT>
class BinarySearchTree {
	TreeNode<keyT, valT>* root;
	// You may add additional private member variables and functions

	//Finding successor of target node
	TreeNode<keyT, valT>* findSuc(TreeNode<keyT, valT>* node){
		while(node&&node->left!=nullptr){
			node = node->left;
		}
		return node;
	}
	//Finding predecessor of target node
	TreeNode<keyT, valT>* findPre(TreeNode<keyT, valT>* node){
                while(node&&node->right!=nullptr){
                        node = node->right;
                }
                return node;
        }
	//Clear root's left and right subtrees then make it null
	void clear(TreeNode<keyT, valT>* node){
		if(node==nullptr) return;
		clear(node->left);
		clear(node->right);
		delete node;
	}
public:
	BinarySearchTree() {
		// Constructor
		root = nullptr;
	}

	~BinarySearchTree() {
		// Destructor
		clear();
	}

	TreeNode<keyT, valT>* insert(keyT key, valT val) {
		// Insert a new node to tree
		TreeNode<keyT, valT>* p = new TreeNode<keyT, valT>(key, val);
		if(root==nullptr){
			root = p;	
		}else {
			//Finding its parent by comparing the key with parent one until there is null child of parent
			TreeNode<keyT, valT>* w;
			TreeNode<keyT, valT>* temp = root;
			while(temp!=nullptr){
				w = temp;
				if(key<w->key){
					temp = temp->left;
				}
				else if(key>w->key){
					temp=temp->right;
				}else{
					//if there is such node then do not insert it
					return nullptr;
				}
			}
			//Last check to make sure to insert it correctly
			if(key<w->key) w->left = p;
			else w->right = p;
			p->parent = w;
		}
		return p;
	}

	bool remove (TreeNode<keyT, valT>* node) {
		// Remove 'node' and return true on success, false on fail
		// For example, if node is nullptr, do nothing and return false
		if(node==nullptr) return false;
		//In case where node is leaf. Node is leaf but not root then find if it is left or right child of its parent and make it null then delete the node.
		//If it is root, then make the root as null
		if(node->left==nullptr&&node->right==nullptr){
			if(node==root) root = nullptr;
			else if(node->parent->left==node) node->parent->left = nullptr;
			else node->parent->right = nullptr;
			delete node;
			return true;
		}
		//In case where node has children
		auto* suc = findSuc(node->right);
		auto* pre = findPre(node->left);
		if(suc){
			//Check if sucessor is node's right child then change its node's right to successor's right and if there is successor's child, assign its parent to successor's parent
			//If it is a successor then check if it has child, assign its parent's left to the child and change child's parent accordingly
			if(suc==node->right) {suc->parent->right = suc->right; if(suc->right){suc->right->parent = suc->parent;}}
			else if(suc->right) {suc->parent->left = suc->right; suc->right->parent = suc->parent;}
			else suc->parent->left = nullptr;
			node->key = suc->key;
			node->val = suc->val;
			delete suc;
		}else if(pre){
			 //Check if predecessor is node's left child then change its node's left to predecessor's left and if there is predecessor's child, assign its parent to pre's parent
                        //If it is a predecessor then check if it has child, assign its parent's right to the child and change child's parent accordingly
			if(pre==node->left) {pre->parent->left = pre->left; if(pre->left){pre->left->parent = pre->parent;}}
                        else if(pre->left) {pre->parent->right = pre->left; pre->left->parent = pre->parent;}
                        else pre->parent->right = nullptr;
                        node->key = pre->key;
                        node->val = pre->val;
			delete pre;
		}
		return true;		
	}

	TreeNode<keyT, valT>* search(keyT key) const {
		// Find the node that has key 'key'
		// If not found, return nullptr
		//Check if there is tree node that has key equal to the input by traversing
		TreeNode<keyT, valT>* temp = root;
		while(temp!=nullptr){
			if(key==temp->key) return temp;
			else if(key<temp->key) temp = temp->left;
			else temp = temp->right;
		}
		return nullptr;
	}

	void clear() {
		// Remove all nodes in the tree
		//Call my own defined clear with parameter root
		clear(root);
		root=nullptr;
	}

	void print_in(TreeNode<keyT, valT>* current) const {
		if (current != nullptr) {
			print_in(current->left);
			std::cout << current->key << ' ' << std::flush;
			print_in(current->right);
		}
	}

	void print_pre(TreeNode<keyT, valT>* current) const {
		if (current != nullptr) {
			std::cout << current->key << ' ';
			print_pre(current->left);
			print_pre(current->right);
		}
	}

	void print_post(TreeNode<keyT, valT>* current) const {
		if (current != nullptr) {
			print_post(current->left);
			print_post(current->right);
			std::cout << current->key << ' ';
		}
	}

	void print() const {
		// It prints all node info in three different ways
		// to make sure all nodes are in the right place
		print_in(this->root);
		std::cout << std::endl;

		print_pre(this->root);
		std::cout << std::endl;

		print_post(this->root);
		std::cout << std::endl;
	}
};

#endif
