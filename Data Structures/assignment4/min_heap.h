#ifndef MIN_HEAP_H
#define MIN_HEAP_H

template <typename T>
struct MinHeap {
	// You can add additional functions


	//I find target's children then I find the minimum between children and the target.
	static void heapify(int index, T* arr, int size){
		int childI = 2*index+1;
		T val = arr[index];
		while(childI<size){
			T minVal = val;
			int minI = -1;
			for(int i = 0;i<2&&i+childI<size;i++){
				if(arr[i+childI]<minVal){
					minVal = arr[i+childI];
					minI = i+childI;
				}
			}
		//If one of children is minimum, I swap it with target. then I go down to that child and find minimum between children and the target's value
		if(minVal==val)	return;
		T temp = arr[index];
		arr[index] = arr[minI];
		arr[minI] = temp;
		index = minI;
		childI = 2*index+1;
		}
	}
	//I compare the target's value with its parent.
	//If parent's value is greater than target's value I swap the values and I make that parent to be the target.
	static void insert(int index, T* arr){
		while(index>0){
			int parentI = (index-1)/2;
			if(arr[index]<arr[parentI]){
				T temp = arr[index];
				arr[index]=arr[parentI];
				arr[parentI] = temp;
				index = parentI;
			}else{
				//If target is less than parent, I stop the loop.
				return;
			}
		}
	}
	//If hint is not given, starting from the first internal node to the root, I heapify the array.
	//If hint is given, I check first if target has parent and target is less than its parent.
	//If target is less than its parent, then I call insert function to swap target with parent
	//If it is not, then I call heapify to swap target with children if necessary.
	static void make_heap(T* arr, int size, int hint = -1) {
		// Build heap
		if(hint==-1){
			for(int i = size/2-1;i>=0;i--){
				heapify(i,arr, size);
			}
		}else{
			if((hint-1)/2>=0&&arr[hint]<arr[(hint-1)/2])
				insert(hint, arr);
			else
				heapify(hint,arr,size);
		}
	}
	//I swap first element with last element of array.
	//Then I call make heap with index 0 and size to be one less.
	static void pop(T* arr, int size) {
		// Delete minimum
		T temp = arr[0];
		arr[0] = arr[size-1];
		arr[size-1]=temp;
		make_heap(arr, size-1, 0);
	}
	//I push the item to the first empty index and I call insert to make sure it will be in right place in case if the item is less than the parent.
	static void push(T* arr, int size, T item) {
		// Push item
		arr[size] = item;
		insert(size, arr);
	}
};
#endif
