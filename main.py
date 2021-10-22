from LanguageSpecification import separators, operators, reservedWords, codification
from ProgramInternalForm import ProgramInternalForm
from Scanner import tokenGenerator, isIdentifier, isConstant
from SymbolTable import SymbolTable

if __name__ == '__main__':
    fileName = input("Insert file name: ")

    file = open(fileName, 'r')
    for line in file:
        print(line)

    with open(fileName, 'r') as file:
        for line in file:
            print([token for token in tokenGenerator(line, separators)])

    symbolTable = SymbolTable()
    pif = ProgramInternalForm()

    with open(fileName, 'r') as file:
        lineNo = 0
        for line in file:
            lineNo += 1
            for token in tokenGenerator(line[0:-1], separators):
                if token in separators + operators + reservedWords:
                    pif.add(token, -1)
                elif isIdentifier(token):
                    _id = symbolTable.add(token)
                    pif.add('identifier: ' + token, _id)
                elif isConstant(token):
                    _id = symbolTable.add(token)
                    pif.add('constant' + token, _id)
                else:
                    raise Exception('Unknown token ' + token + ' at line ' + str(lineNo))

    print('Program Internal Form: \n', pif)
    print('Symbol Table: \n', symbolTable)
