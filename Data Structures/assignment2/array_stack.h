template <class T>
class ArrayStack {
    T* _array;
    int capacity = 100000;
    int length;
    // You may add member variables.

public:
    explicit ArrayStack() {
        // Constructor. Initialize member variables, etc.
	length = -1;
	_array = new T[capacity];
    }

    ~ArrayStack() {
        // Destructor. Release resources, etc.
	delete [] _array;
    }

    T& top() {
        // Return top element
	return _array[length];
    }

    void pop() {
        // Remove top element
 	length--;
    }

    bool empty() {
        // Return true if empty, false otherwise
	if(length==-1){
		return true;
	}
	return false;
    }

    int size() {
        // Return number of elements
    	return length+1;	
    }

    void push(T& item) {
        // Add a new item at the top
	if(length==capacity-1){
		T* tempA = new T[capacity*2];
		for(int i = 0; i<capacity; i++){
			tempA[i] = _array[i];
		}
		capacity*=2;
		delete [] _array;
		_array = tempA;
	}
	length++;
	_array[length]=item;
    }

    // You may add other member functions
};
