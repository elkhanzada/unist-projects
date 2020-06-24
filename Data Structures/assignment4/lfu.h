#ifndef LFU_H
#define LFU_H

#include "min_heap.h"

template <typename T>
struct CacheItem {
	int usedCount;  // The number of accesses after inserted to the cache.
	T item;

	explicit CacheItem(T _item = T(), int _usedCount = 0) {
		usedCount = _usedCount;
		item = _item;
	}

	bool operator == (const CacheItem<T> &other) const {
		return item == other.item;
	}

	bool operator < (const CacheItem<T> &other) const {
		return usedCount < other.usedCount;
	}

	bool operator > (const CacheItem<T> &other) const {
		return usedCount > other.usedCount;
	}
};

template <typename T>
class LFU {
	CacheItem<T>* cache;
	const int size;    // cache size
	int misses;   
	int length;  //current length
	int index;   //hint

	// You can add private member variables and functions.

public:
	LFU(int _size) : size(_size) {
		// Constructor
		cache = new CacheItem<T>[_size];
		misses = 0;
		length = 0;
	}

	~LFU() {
		// Destructor
		delete cache;
	}

	bool exists(T item) {
		// Return true if data exists in the cache
		// Return false otherwise
		for(int i =0;i<length;i++)
			if(cache[i].item==item){
			//To store the index, I made index variable.
				index = i;
				return true;
			}
		return false;
		
	}
	
	int status() const {
		// Return number of elements in cache
		return length;
	}
	//If item exists, then I increase usedCount of it by one and I call make heap with the index given by Exists function
	//If it does not exit, then I increase misses by one, check whether cache is full.
	//If cache is full, I change the root with new item and return false.
	//If it is not, I call push function with old length as index and I increase length by one, return false.
	bool touch(T item) {
		// The data is being accessed
		// Return true on hit, false on miss
		// i.e. return true if it existed, and false when it was not
		if(exists(item)){
			cache[index].usedCount+=1;
			MinHeap<CacheItem<T>>::make_heap(cache, length, index);
			return true;
		}
		misses++;
		if(status()==size){
			CacheItem<T> temp(item);
			cache[0] = temp;
			return false;
		}

		CacheItem<T> temp(item);
		MinHeap<CacheItem<T>>::push(cache, length, temp);
		length++; 
		return false;
	}

	int getMisses() {
		// Return the number of cache misses until now
		return misses;
	}
	void display() {
		for(int i = 0;i<size;i++){
			std::cout<<"["<<cache[i].item<<"] = "<<cache[i].usedCount<<"\n";
		}
	}
};
#endif
