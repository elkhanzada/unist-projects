#include <stdio.h>

int data[] = {8,5,14,10,12,3,9,6,1,15,7,4,13,2,11};
int size = 15;


//Below function is for debugging purpose only. Don't implement this
/*
void debug(){
	int i;
	for(i=0;i<size;i++)
		printf("%d, ", data[i]);	

	printf("\n");
}
*/

int partition(int *data, int start, int end){
	int left=start;
	int right=end;
	int pivot=data[start];

	while(left<right){

		while (data[right] > pivot){
			right--;
		}

		while((left < right) && (data[left] <= pivot)){
			left++;
		}

		if(left<right){
			int temp = data[right];
			data[right] = data[left];
			data[left] = temp;
		}
	}

	data[start]=data[right];
	data[right]=pivot;

	return right;
}

void quick_sort(int *data, int start, int end){
	int pivot_position;

	if(start < end){
		pivot_position = partition(data, start, end);
		quick_sort(data, start, pivot_position-1);
		quick_sort(data, pivot_position+1, end);
	}
}
void main(){
	quick_sort(data,0,size-1);
	//debug();
}
