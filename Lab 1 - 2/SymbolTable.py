from HashTable import HashTable


class SymbolTable:
    def __init__(self):
        self.table = HashTable()

    def add(self, value):
        return self.table.insert(value)

    def get_symbol(self, index):
        node = self.table.find(index)
        list_of_symbols = []
        while node is not None:
            list_of_symbols.append(node.value)
            node = node.next
        return list_of_symbols

    def get_index(self, value):
        index, sub_index = self.table.get_index(value)
        return index, sub_index

    def __str__(self):
        string = "========================\n"
        for element in self.table.buckets:
            if element is not None:
                string += str(self.get_index(element.value)[0])
                string += " | "
                string += str(element) + "\n"
        string += "========================\n"
        return string
