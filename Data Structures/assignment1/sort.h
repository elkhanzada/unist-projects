void sort(int* numbers) {
	// implement your sorting algorithm
	int n = 10000;
	int min = 0;
	for (int i = 0; i<n-1;i++){
		int minIndex = i;
		for (int j = i; j<n;j++)
			if(numbers[minIndex]>numbers[j])
				minIndex = j;
			
		
		int temp = numbers[i];
		numbers[i]=numbers[minIndex];
		numbers[minIndex]=temp;
		
	}
}

// Add functions if you need to
