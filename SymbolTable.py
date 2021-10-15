from HashTable import HashTable


class SymbolTable:
    def __init__(self):
        self.table = HashTable()

    def add(self, value):
        self.table.insert(value)

    def get(self, value):
        self.table.get_id(value)
