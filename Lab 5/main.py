from model.grammar import Grammar

if __name__ == '__main__':
    grammar = Grammar('resources/g2.txt')
    print("Grammar: ", grammar.to_string(), "\n")
    print("Set of nonterminals: \n" + str(grammar.non_terminals), "\n")
    print("Set of terminals: \n" + str(grammar.terminals), "\n")
    production_string = ""
    for production in grammar.productions:
        production_string += str(production)
    print("Set of productions: \n" + production_string, "\n")

    print("Is CFG?: ", grammar.CFG_check())

    non_terminal = input("Enter the given nonterminal to show the production for: ")
    production_string = ""
    for production in grammar.get_productions_for_non_terminal(non_terminal):
        production_string += str(production)
    print("The production is: \n" + production_string, "\n")
