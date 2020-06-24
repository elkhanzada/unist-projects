#ifndef BPlusTree_H
#define BPlusTree_H

#include <iostream>

template <typename T>
struct Node {
    bool is_leaf;
    std::size_t degree; // maximum number of children
    std::size_t size; // current number of items
    T* item;
    Node<T>** children; 
    Node<T>* parent; //Self-explanatory
    Node<T>* next; //Used for connecting leaf nodes
    // You may add variables if needed.

public:
    Node(std::size_t degree) {
        // Constructor
        is_leaf = true;
        item = new T[degree];
        children  = new Node<T>*[degree+1];
        size = 1;
        parent = nullptr; 
        next = nullptr; 
    }
    // You may add a destructor if needed.
    ~Node(){
    	parent = nullptr;
    	next = nullptr;
    }
};

template <typename T>
class BPlusTree {
    Node<T>* root;
    std::size_t deg;
    
    //I check whether data exists in the array of range search so that there are no duplicate elements    
    bool exists(T* arr, T data, int len) {
   	for(std::size_t i = 0; i<len; i++)
   		if(data == arr[i])
   			return true;
   	return false;
   }
    //This is used for cleaning the tree and it is called when destructor is called. It goes through all the children and deletes their children as well as the items
    void clean(Node<T>* cur){
    	if(cur!=nullptr){
		if(cur->is_leaf==false){
			std::size_t len = cur->size+1;
			for(std::size_t i = 0; i<len; i++){
				 	clean(cur->children[i]);
				 	cur->children[i] = nullptr;
			 }
		}
		delete[] cur->children;
		delete[] cur->item;
		delete cur;
	}
    }
    //This function perform merging in case if the siblings have less few keys
    //It can perform merging  with left as well as right sibling
    //I first find the index in which parent's children points to the cur node
    //From there I find the sibling
    //If cur node is not a leaf then it takes item from its parent
    //I insert the items from sibling to cur node
    //If cur is internal node then it takes the children of the sibling
    //If cur is leaf then after merging, cur's next leaf points to the sibling's next leaf
    Node<T>* mergeWith(Node<T>* cur){
    	auto* parentNode = cur->parent;
    	std::size_t parentIndex =0 ;
    	for(parentIndex = 0; parentNode->children[parentIndex]!=cur; parentIndex++);
    	auto* sibling = parentNode->children[parentIndex+1];
	if(cur->is_leaf==false){
		cur->item[cur->size] =parentNode->item[parentIndex];
	}
	std::size_t insertIndex;
	for(std::size_t i = 0; i<sibling->size; i++){
		insertIndex = cur->size+1+i;
		if(cur->is_leaf)
			insertIndex--;
		cur->item[insertIndex] = sibling->item[i];
	}
	if(cur->is_leaf==false){
		for(std::size_t i = 0; i<=sibling->size; i++){
			cur->children[cur->size+1+i] = sibling->children[i];
			cur->children[cur->size+1+i]->parent = cur;
		}
		cur->size+=sibling->size+1;
		
	}else{
		cur->size+=sibling->size;
		cur->next = sibling->next;
		
	}
	for(std::size_t i = parentIndex+1; i<parentNode->size; i++){
		parentNode->children[i] = parentNode->children[i+1];
		parentNode->item[i-1] = parentNode->item[i];
	}
	parentNode->size--;  
	return cur; 	
    }
    //In this function, I take item from right sibling
    //I increase the size of cur node and if it is leaf then the last item of cur will be the smallest element of right sibling
    //If it is internal node, then the last item of cur will be its parent's item at the index where parent's children pointer points to the cur node
    //In the end I decrease the size of right sibling
    Node<T>* takeFromRight(Node<T>* cur, std::size_t parentIndex){
    	auto* parentNode=cur->parent;
    	auto* right = parentNode->children[parentIndex+1];
    	cur->size++;
    	if(cur->is_leaf){
    		cur->item[cur->size-1] = right->item[0];
    		parentNode->item[parentIndex] = right->item[1];
    		
    	}else{
    		cur->item[cur->size-1] = parentNode->item[parentIndex];
    		parentNode->item[parentIndex] = right->item[0];
    	}
    	if(cur->is_leaf==false){
    		cur->children[cur->size] = right->children[0];
    		cur->children[cur->size]->parent = cur;
    		for(std::size_t i = 1; i<right->size+1; i++){
    			right->children[i-1] = right->children[i];
    		}
    	}
    	for(std::size_t i = 1; i<right->size; i++){
    		right->item[i-1] = right->item[i];
    	}
    	right->size--;
    	return cur;
    
    }
    //In this function, I take item from left sibling
    //I increase the size of cur node and move the items one step forward so that to make space for new item
    //If the cur node is leaf, then first element of cur node will be the last element of left sibling
    //If it is internal node, then the first element of cur node will be the parentNode's item at index in which parentNode's children pointer points to cur's left sibling
    //In the end I decrease the size of left sibling
    Node<T>* takeFromLeft(Node<T>* cur, std::size_t parentIndex){
    	auto* parentNode = cur->parent;
    	cur->size++;
    	for(std::size_t i = cur->size-1; i>0;i--)
    		cur->item[i]=cur->item[i-1];
    	auto* left = parentNode->children[parentIndex-1];
    	if(cur->is_leaf){
    	  	cur->item[0] = left->item[left->size-1];
    		parentNode->item[parentIndex-1]=left->item[left->size-1];
    	}else{
    		cur->item[0]=parentNode->item[parentIndex-1];
    		parentNode->item[parentIndex-1]=left->item[left->size-1];
    	}
    	if(cur->is_leaf==false){
    		for(std::size_t i = cur->size; i>0; i--)
    		{
    			cur->children[i]=cur->children[i-1];
    		}
    		cur->children[0] = left->children[left->size];
    		left->children[left->size] = nullptr;
    		cur->children[0]->parent= cur;
    	}
    	left->size--;
    	return cur;
    }
    //In this function, after deleting the item and reducing the size of cur node, I try to repair it
    //If the size is deficient I check if it is root node
    //If it is root node I change root to point to cur's first children and I make root's parent null
    //If not I find its parent and index that parentNode's children pointer points to the cur node
    //If parentIndex is positive and left sibling has enough items then I take item from it
    //If parentIndex is positive and right sibling has enough items then I take item from it
    //If none works and the cur node is the first children of parent node then I merge it with its right sibling
    //If not, it means the cur node has left sibling so I merge it with left sibling
    void repairAfterDelete(Node<T>* cur){
    	if(cur->size<(deg+1)/2-1){
    		if(cur->parent==nullptr)
    		{
    			if(cur->size==0)
    			{	
    				root=cur->children[0];
    				if(root)
    					root->parent=nullptr;
    			}
    		}else{
    			auto* parentNode = cur->parent;
    			std::size_t parentIndex;
    			for(parentIndex=0;parentNode->children[parentIndex]!=cur;parentIndex++);
    			if(parentIndex>0&&parentNode->children[parentIndex-1]->size>=(deg-1)/2+1)
    				takeFromLeft(cur, parentIndex);
    			else if(parentIndex<parentNode->size&&parentNode->children[parentIndex+1]->size>=(deg-1)/2+1)
    				takeFromRight(cur, parentIndex);
    			else if(parentIndex==0){
    				auto* nextNode = mergeWith(cur);
    				repairAfterDelete(nextNode->parent);
    			}else{
    				auto* nextNode = mergeWith(parentNode->children[parentIndex-1]);
    				repairAfterDelete(nextNode->parent);
    			}
    		}
    	}
    }
    //In this function, I decrease the size of the cur node that contains the data
    //For this, I recursively call the function to the cur node that has this data
    //After finding it, and making sure it is leaf node, I move items one step backward
    //I call repair if it is deficient node
    void deleteNode(Node<T>* cur, T data){
    if(cur){
    	std::size_t i;
    	for(i = 0; i<cur->size&&cur->item[i]<data;i++);
    	if(i==cur->size){
    		if(cur->is_leaf == false){
    			deleteNode(cur->children[cur->size], data);
    		}
    	}else if(cur->is_leaf==false&&cur->item[i]==data){
    		deleteNode(cur->children[i+1], data);
    	}
    	else if(cur->is_leaf==false){
    		deleteNode(cur->children[i], data);
    	}else if(cur->is_leaf && cur->item[i]==data){
    		for(std::size_t j = i;j<cur->size-1; j++){
    			cur->item[j]=cur->item[j+1];
    		}
    		cur->size--;
    		repairAfterDelete(cur);
    		}	
    	}
    	}
    	
    
    //This function splits the node in case if the size is full
    //I create new node that will be right node which will take cur node's second half of items
    //I get the parent and parentIndex for cur node
    //I increase the size of parentNode and add the item of cur that is in middle to parentNode's item at the parentIndex
    //I make sure that this right node's parent is the cur node's parentNode
    //If cur node is leaf then right node 's next points to cur node's next
    //And cur node's next points to right node
    //After children pointer manipulations, I return cur node's parent if it has one
    //If it does not, then I create new root node and the old root points to the new one
    //In the end I return the root node.
    
    Node<T>* split(Node<T>* cur){
    	auto* rNode = new Node<T>(deg);
    	T upItem = cur->item[deg/2];
    	std::size_t i, parentIndex;
    	if(cur->parent){
    		auto* curParent = cur->parent;
    		for(parentIndex = 0; parentIndex<curParent->size+1; parentIndex++)
    				if(curParent->children[parentIndex]==cur)
    					break;
    		for(i = curParent->size; i>parentIndex; i--){
    			curParent->children[i+1]=curParent->children[i];
    			curParent->item[i] = curParent->item[i-1];
    		}
    		curParent->size++;
    		curParent->item[parentIndex] = upItem;
    		curParent->children[parentIndex+1] = rNode;
    		rNode->parent=curParent;
    	}
    	std::size_t rSplit;
    	if(cur->is_leaf){
    		rSplit = deg/2;
    		rNode->next = cur->next;
    		cur->next = rNode;
    	}else{
    		rSplit = deg/2+1;
    	}
    	rNode->size = cur->size-rSplit;
    	for(i  = rSplit; i<cur->size+1;i++){
    		rNode->children[i-rSplit] = cur->children[i];
    		if(cur->children[i]){
    			rNode->is_leaf = false;
    			cur->children[i]->parent = rNode;
    			cur->children[i] = nullptr;
    		}	
    	}
    	for(i = rSplit; i<cur->size; i++){
    		rNode->item[i-rSplit] = cur->item[i];
    	}
    	auto* lNode = cur;
    	lNode->size = deg/2;
    	if(cur->parent){
    		return cur->parent;
    	}
    	auto* nRoot = new Node<T>(deg);
    	nRoot->item[0] = upItem;
    	nRoot->children[0] = lNode;
    	nRoot->children[1] = rNode;
    	root = nRoot;
    	lNode->parent = root;
    	rNode->parent = root;
    	root->is_leaf = false;
    	return root;
    }
    //In this function I split the every node that needs it by calling recursively
    //If cur node's size is big, I call split and if it has no parent then I assign root to the new splitted node
    //If it has parent then I assign splitted node to new node and I call repair recursively in case if that new node has more items.
    void repair(Node<T>* cur){
    	if(cur->size<=deg-1) return;
    	if(cur->parent==nullptr){
    		root = split(cur);
    		return;
    	}
    	auto* newNode = split(cur);
    	repair(newNode);
    
    }
    //If cur node is leaf then I increase the size and I find insertIndex to insert new data and I call repair if it has more items.
    //If it is not leaf then I find index in which cur's item is less than the data and greater than previous items and if it has children at that index I call insert recursively with that children and the data.
    void insert(Node<T>* cur, T data){
    	if(cur->is_leaf){
    		cur->size++;
    		std::size_t insertIndex = cur->size-1;
    		while(insertIndex>0&&cur->item[insertIndex-1]>data){
    			cur->item[insertIndex] = cur->item[insertIndex-1];
    			insertIndex--;
    		}
    		cur->item[insertIndex] = data;
    		repair(cur);
    		return;
    	}
    	std::size_t findIndex = 0;
    	while(findIndex<cur->size&&cur->item[findIndex]<data){
		findIndex++;
	}
	if(cur->children[findIndex])
	insert(cur->children[findIndex], data);
    }
public:
    BPlusTree(std::size_t degree) {
        // Constructor
        deg = degree;
        root = nullptr;
    }

    ~BPlusTree() {
        // Destructor
        clean(root);
    }
    //In this function, I check whether data is less than cur node's item and if it is then it is in the left subtree so I go down
    //If I reach the end of item list then I go to right subtree
    
    bool search(T data) {
        // Return true if the item exists. Return false if it does not.
	if(!root) return false;
	auto* cur = root;
	while(cur->is_leaf==false){
		for(std::size_t i =0;i<cur->size;i++){
			if(data<cur->item[i]){
				cur=cur->children[i];
				break;
			}
			if(i==cur->size-1){
				cur = cur->children[i+1];
				break;
			}
		}
	}
	for(std::size_t i = 0; i<cur->size;i++){
		if(cur->item[i]==data) return true;
	}
	return false;
    }
   //I first check if data is already in the tree
   //If it is not I check whether root is null
   //If it is null then I make root node and add the item to it
   //If it is not then I can insert with root and data as parameters.
    void insert(T data) {
        // Insert new item into the tree.
        if(search(data)) return;
        if(!root){
        	root = new Node<T>(deg);
        	root->item[0] = data;
        	root->is_leaf = true;
        	return;
        }
        insert(root, data);
    }

    void remove(T data) {
        // Remove an item from the tree.
        deleteNode(root, data);
        if(!root) return;
        if(root->size==0){
        	root = root->children[0];
        	root->parent = nullptr;
        }
    }

    //First I check if root is null and if it is then return 0
    //I search for the the node that may have start item
    //After this I go to next leaf node starting from the found one and find the items that is in range and add it to the result array till the size is full but I do also check whether it exists in result array to avoid duplicates
    int range_search(T start, T end, T* result_data, int arr_length) {
        // Implement here
        auto* cur = root;
        int count = 0;
        if(!root) return 0;
        while(cur->is_leaf==false){
		for(std::size_t i =0;i<cur->size;i++){
			if(start<=cur->item[i]){
				cur=cur->children[i];
				break;
			}
			if(i==cur->size-1){
				cur = cur->children[i+1];
				break;
			}
		}
	}
	
	while(cur){
		for(std::size_t i = 0; i<cur->size; i++){
			if(count==arr_length) return -1;
			if(cur->item[i]>=start&&cur->item[i]<=end){
				if(!exists(result_data, cur->item[i], arr_length))
				result_data[count++] = cur->item[i];
			}

		}
	 	cur = cur->next;
	}
	return count;
    }
    Node<T>* getRoot(){
    	return root;
    }

    void print(Node<T>* cursor) {
        // You must NOT edit this function.
        if (cursor != NULL) {
            for (int i = 0; i < cursor->size; ++i) {
                std::cout << cursor->item[i] << " ";
            }
            std::cout << "\n";

            if (cursor->is_leaf != true) {
                for (int i = 0; i < cursor->size + 1; ++i) {
                    print(cursor->children[i]);
                }
            }
        }
    }
};

#endif
