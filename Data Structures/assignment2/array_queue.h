template <class T>
class ArrayQueue {
    T* _array;
    int frontEl;
    int rear;
    int length;
    int capacity = 100000;
    // You may add member variables.

public:
    ArrayQueue() {
        // Constructor. Initialize member variables, etc.
	length = 0;
	_array = new T[capacity];
	frontEl = 0;
	rear = 0;
	
    }

    ~ArrayQueue() {
        // Destructor. Release resources, etc.
	delete [] _array;
    }

    T& front() {
        // Return first element
	return _array[frontEl+1];
    }


    void pop() {
        // Remove first element
	frontEl = (frontEl+1)%capacity;
	length-=1;
    }


    bool empty() {
        // Return true if empty, false otherwise
	if(frontEl==rear){
		return true;
	}
	return false;
    }


    int size() {
        // Return number of elements
	return length;
    }

    void push(T& item) {
        // Add a new item at the end of queue
	if((rear+1)%capacity==frontEl){
		T* tempA = new T[capacity*2];
		for(int i = 0; i<capacity; i++){
			tempA[i] = _array[i];
		}
		delete [] _array;
		_array = tempA;
		rear = capacity;
		_array[rear]=item;
		capacity*=2;
	}
	else {
		rear = (rear+1)%capacity;
		_array[rear]=item;
	}
	length+=1;
    }

    // You may add other member functions
};
