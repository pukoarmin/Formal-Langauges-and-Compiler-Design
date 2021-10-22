separators = ['[', ']', '(', ')', ' ', ':', ';']
operators = ['+', '-', '/', '%', '<', '<=', '=', '>',
             '==', '++', '--', ',']
reservedWords = ['sqrt', 'Integer', 'Boolean', 'for', 'if', 'else',
                 'print', 'BEGIN', 'END', 'String', 'read', 'and', 'Struct',
                 'List']

everything = separators + operators + reservedWords
codification = dict([(everything[i], i + 2) for i in range(len(everything))])
codification['identifier'] = 0
codification['constant'] = 1
