class ProgramInternalForm:
    def __init__(self):
        self.__content = []

    def add(self, token, _id):
        self.__content.append((token, _id))

    def __str__(self):
        string = "========================\n"
        for element in self.__content:
            string += str(element) + "\n"
        string += "========================\n"
        return string
