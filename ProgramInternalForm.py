class ProgramInternalForm:
    def __init__(self):
        self.__content = []

    def add(self, code, _id):
        self.__content.append((code, _id))

    def __str__(self):
        string = ""
        for element in self.__content:
            string += str(element) + "\n"
        return string
