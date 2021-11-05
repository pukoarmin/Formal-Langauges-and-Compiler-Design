INITIAL_CAPACITY = 256


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        string = ""
        string += self.value
        node = self.next
        while node is not None:
            string += ", " + node.value
            node = node.next
        return string


# Hash table with separate chaining
class HashTable(object):
    def __init__(self):
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, value):
        hash_sum = 0
        # For each character in the value
        for index, character in enumerate(value):
            # Add (index + length of value) ^ (current char code)
            hash_sum += (index + len(value)) ** ord(character)
            # Perform modulus to keep hash_sum in range [0, self.capacity - 1]
            hash_sum = hash_sum % self.capacity
        return hash_sum

    def insert(self, value):
        # 1. Increment size
        self.size += 1
        # 2. Compute index of value
        index = self.hash(value)
        # Go to the node corresponding to the hash
        node = self.buckets[index]

        # 3. If bucket is empty:
        if node is None:
            # Create node, add it, return
            self.buckets[index] = Node(value)
            return index

        # 4. Collision! Iterate to the end of the linked list at provided index
        prev = node
        sub_pos = 0
        while node is not None:
            if node.value != value:
                sub_pos += 1
                prev = node
                node = node.next
            else:
                return [index, sub_pos]
        # Add a new node at the end of the list with provided value
        prev.next = Node(value)
        return [index, sub_pos]

    def get_index(self, value):
        # 1. Compute hash
        index = self.hash(value)
        sub_pos = 0
        # 2. Go to first node in list at bucket
        node = self.buckets[index]
        # 3. Traverse the linked list at this node
        while node is not None and node.value != value:
            sub_pos += 1
            node = node.next
        # 4. Now, node is the requested value/value pair or None
        if node is None:
            # Not found
            return None, None
        else:
            # Found - return the data value
            return index, sub_pos

    def find(self, index):
        return self.buckets[index]

    def remove(self, value):
        # 1. Compute hash
        index = self.hash(value)
        node = self.buckets[index]
        prev = None
        # 2. Iterate to the requested node
        while node is not None and node.value != value:
            prev = node
            node = node.next
        # Now, node is either the requested node or none
        if node is None:
            # 3. value not found
            return None
        else:
            # 4. The value was found.
            self.size -= 1
            result = node.value
            # Delete this element in linked list
            if prev is None:
                self.buckets[index] = node.next  # May be None, or the next match
            else:
                prev.next = prev.next.next  # LinkedList delete by skipping over
            # Return the deleted result
            return result
