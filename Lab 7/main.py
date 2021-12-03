from model.grammar import Grammar
from model.parser import Parser

if __name__ == '__main__':
    grammar = Grammar('resources/g2.txt')
    parser = Parser(grammar)
    parser.parse()
