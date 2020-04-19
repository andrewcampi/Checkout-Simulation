
#Andrew Campi
#EventQueue.py
#04/11/20
#Phase 1

class EventQueue:
    def __init__(self,num_levels):
        """Creates a priority queue."""
        self._size = 0
        self._capacity = num_levels * 2
        self.data = []
        for x in range(self._capacity+1):
           self.data.append([])
    
    def is_empty(self):
        """Returns True if no items are in the event queue. Else, returns False."""
        return self._size == 0

    def __len__(self):
        """Returns the number of items in the event queue."""
        return self._size
    
    def insert(self,item,priority):
        """Inserts a given item at a given priority."""
        assert priority >= 0 and priority < self._capacity , "Invalid priority level."
        self.data[priority].append(item)
        self._size += 1
    
    def delete(self):
        """Removes and returns the next item in the event queue."""
        assert self._size > 0 , "Cannot delete item from an empty event queue."
        item_found = False
        current_index = 0
        item_to_return = None
        while not item_found:
            if (self.data[current_index] != []):          #If priority is occupied by an item
                item_found = True
                item_to_return = self.data[current_index][0]
                if (len(self.data[current_index]) >= 1):
                    self.data[current_index].pop(0)           #Delete item from event queue.
                self._size -= 1
            else:
                current_index += 1
        return item_to_return, current_index
    
    def peek_next(self):
        """Return the priority value of the next item to be removed from event queue."""
        assert self._size > 0 , "Cannot delete item from an empty event queue."
        item_found = False
        current_index = 0
        item_to_return = None
        while not item_found:
            if (self.data[current_index] != []):          #If priority is occupied by an item
                item_found = True
                item_to_return = self.data[current_index][0]
            else:
                current_index += 1
        return current_index
    
        
    def __str__(self):
        """Returns string version of event queue."""
        to_return = ""
        for x in range(len(self.data)):
            if (self.data[x] != []):  #If priority is occupied by an item
                this_item = ""
                this_item += "Priority ["
                this_item += str(x)
                this_item += "] = "
                this_item += str(self.data[x])
                to_return += this_item
                to_return += "\n"
        return to_return
