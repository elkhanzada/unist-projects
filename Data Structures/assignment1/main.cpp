#include <iostream>
#include <fstream>
#include "sort.h"

#define N 10000

void print(int* nums) {
	for(int i=0; i<N; ++i) {
		std::cout << nums[i] << '\n';
	}
}

int main(void) {
	std::ifstream ifs("input1.txt");
	if(!ifs.is_open()) {
		std::cerr << "INPUT ERROR\n" << std::endl;
		return -1;
	}
	
	int nums[N];
	for(int i=0; i<N; ++i) {
		ifs >> nums[i];
	}
	ifs.close();
	
	std::cout << "[BEFORE]: ";
	print(nums);
	
	sort(nums); // you should implement this function
	
	std::cout << "[AFTER]: ";
	print(nums);
	
	return 0;
}
