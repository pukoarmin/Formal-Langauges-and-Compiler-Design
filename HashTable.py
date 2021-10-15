INITIAL_CAPACITY = 256


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "%s, %s" % (self.value, self.next is not None)

    def __repr__(self):
        return str(self)


# Hash table with separate chaining
class HashTable(object):
    def __init__(self):
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, key):
        hash_sum = 0
        # For each character in the key
        for index, character in enumerate(key):
            # Add (index + length of key) ^ (current char code)
            hash_sum += (index + len(key)) ** ord(character)
            # Perform modulus to keep hash_sum in range [0, self.capacity - 1]
            hash_sum = hash_sum % self.capacity
        return hash_sum

    def insert(self, key):
        # 1. Increment size
        self.size += 1
        # 2. Compute index of key
        index = self.hash(key)
        # Go to the node corresponding to the hash
        node = self.buckets[index]

        # 3. If bucket is empty:
        if node is None:
            # Create node, add it, return
            self.buckets[index] = Node(key)
            return

        # 4. Collision! Iterate to the end of the linked list at provided index
        prev = node
        while node is not None:
            prev = node
            node = node.next
        # Add a new node at the end of the list with provided key/value
        prev.next = Node(key)

    def get_id(self, key):
        # 1. Compute hash
        index = self.hash(key)
        sub_pos = 0
        # 2. Go to first node in list at bucket
        node = self.buckets[index]
        # 3. Traverse the linked list at this node
        while node is not None and node.key != key:
            sub_pos += 1
            node = node.next
        # 4. Now, node is the requested key/value pair or None
        if node is None:
            # Not found
            return None, None
        else:
            # Found - return the data value
            return index, sub_pos

    def find(self, key):
        # 1. Compute hash
        index = self.hash(key)
        # 2. Go to first node in list at bucket
        node = self.buckets[index]
        # 3. Traverse the linked list at this node
        while node is not None and node.key != key:
            node = node.next
        # 4. Now, node is the requested key/value pair or None
        if node is None:
            # Not found
            return None
        else:
            # Found - return the data value
            return node.value

    def remove(self, key):
        # 1. Compute hash
        index = self.hash(key)
        node = self.buckets[index]
        prev = None
        # 2. Iterate to the requested node
        while node is not None and node.key != key:
            prev = node
            node = node.next
        # Now, node is either the requested node or none
        if node is None:
            # 3. Key not found
            return None
        else:
            # 4. The key was found.
            self.size -= 1
            result = node.value
            # Delete this element in linked list
            if prev is None:
                self.buckets[index] = node.next  # May be None, or the next match
            else:
                prev.next = prev.next.next  # LinkedList delete by skipping over
            # Return the deleted result
            return result
