
#Andrew Campi
#CustomerQueue.py
#04/11/20
#Phase 1


class CustomerQueue:
    def __init__(self):
        """Creates an empty queue."""
        self._list = []
        self._size = 0
    
    def enqueue(self,x):
        """Adds a given item to the queue."""
        self._list.append(x)
        self._size += 1
    
    def dequeue(self):
        """Removes the item at index 0 of the queue"""
        assert not self.is_empty(), "Can't Dequeue from an empty queue."
        self._size -= 1
        return self._list.pop(0)
    
    def peek(self):
        """Returns the item that will be removed the next time dequeue() is called."""
        assert not self.is_empty(), "Can't Peek from an empty queue."
        return self._list[0]
    
    def is_empty(self):
        """Returns True if the queue is empty. Else, returns False."""
        if self._size > 0 :
            return False
        else:
            return True
    
    def __str__(self):
        """Returns a string representation of the queue."""
        return str(self._list)
    
    def __len__(self):
        return len(self._list)