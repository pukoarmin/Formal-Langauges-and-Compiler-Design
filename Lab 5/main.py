from model.grammar import Grammar

if __name__ == '__main__':
    grammar = Grammar('resources/g1.txt')
    print("Grammar: ", grammar.to_string())
    print("Set of nonterminals: \n" + str(grammar.non_terminals))
    print("Set of terminals: \n" + str(grammar.terminals))
    production_string = ""
    for production in grammar.productions:
        production_string += str(production)
    print("Set of productions: \n" + production_string)

    non_terminal = input("Enter the given nonterminal to show the production for: ")
    print("The production is: " + str(grammar.get_productions_for_non_terminal(non_terminal)))
