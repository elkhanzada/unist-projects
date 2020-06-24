#ifndef RAND_H
#define RAND_H

#include <iostream>
#include <random>

class Rand {
    int* arr;
    int size;
    int misses;
    int length;
    std::default_random_engine gen;
    std::uniform_int_distribution<int>* dis;

	// You may add additional private member variables and functions
public:
	Rand(int _size) {
	    // Constructor
	 	size = _size;
		arr = new int[_size];
		misses = 0;
		length = 0;
		dis = new std::uniform_int_distribution<int>(0, size-1);    
}

	~Rand() {
	    // Destructor
	    delete [] arr;
	    delete dis;
	}

	bool exists(int data) {
		// Return true if data exists in the cache
		// Return false otherwise
		for(int i = 0; i<size;i++){
				if(arr[i]==data){
					return true;
				}
		}
		return false;
	}

    int status() {
        // Return the number of elements in cache
	return length;	
    }

	bool touch(int data) {
		// The data is being used
		// Return true on hit, false on miss
		// i.e. return true if it existed, and false when it was not
		if(exists(data))
			return true;	
		misses++;
		//if cache is full, generate random index and assign the data at that index
		if(status()==size){
			int num = (*dis)(gen);
			arr[num] = data;
			return false;
		}
		//if not the increase length and assign it to the last empty place of array
		arr[length++] = data;
		return false;
	}

    int get_misses() {
        // Return the number of cache misses until now
    		return misses;
	}

	void print(void) const {
        for (int i = 0; i < length; i++) {
                std::cout << arr[i] << ' ';
            
        }
        std::cout << '\n';
	}
};

#endif
