from LanguageSpecification import separators, operators, reservedWords
from ProgramInternalForm import ProgramInternalForm
from Scanner import tokenGenerator, isIdentifier, isConstant, isSystemToken
from SymbolTable import SymbolTable


if __name__ == '__main__':
    fileName = input("Insert file name: ")

    file = open(fileName, 'r')
    for line in file:
        print(line)
    print('\n')
    with open(fileName, 'r') as file:
        for line in file:
            print([token for token in tokenGenerator(line, separators)])

    print('\n')
    symbolTable = SymbolTable()
    pif = ProgramInternalForm()

    with open(fileName, 'r') as file:
        lineNo = 0
        for line in file:
            lineNo += 1
            previous_token = None
            for token in tokenGenerator(line[0:-1], separators):
                if isSystemToken(previous_token, token, lineNo):
                    pif.add(token, -1)
                elif isIdentifier(token):
                    _id = symbolTable.add(token)
                    pif.add('identifier: ' + token, _id)
                elif isConstant(token):
                    _id = symbolTable.add(token)
                    pif.add('constant: ' + token, _id)
                else:
                    raise Exception('Unknown token: ' + token + ' at line ' + str(lineNo))
                if token not in separators:
                    previous_token = token

    print('Program Internal Form: \n', pif)
    print('Symbol Table: \n', symbolTable)
