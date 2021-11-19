from model.production import Production


class Grammar:
    def __init__(self, input_file):
        self.non_terminals = []
        self.terminals = []
        self.productions = []
        self.starting_symbol = ""
        self.get_grammar_from_file(input_file)

    def get_grammar_from_file(self, input_file):
        try:
            line_index = 0
            grammar_file = open(input_file)
            for line in grammar_file.readlines():
                if line_index <= 2:
                    tokens = line.split(" ")
                    for token in tokens:
                        if line_index == 0:
                            self.non_terminals.append(token)
                        if line_index == 1:
                            self.terminals.append(token)
                        if line_index == 2:
                            self.starting_symbol = token
                if line_index > 2:
                    tokens = line.split(" -> ")
                    rules = []
                    for rule in tokens[1].split("\\| "):
                        rules.append(rule.split(" "))
                    self.productions.append(Production(tokens[0], rules))
                line_index += 1
        except Exception as e:
            print(e)

    def get_productions_containing_non_terminal(self, non_terminal):
        productions_for_non_terminal = []
        for production in self.productions:
            for rule in production.rules:
                try:
                    if rule.index(non_terminal):
                        productions_for_non_terminal.append(production)
                except:
                    pass

    def get_productions_for_non_terminal(self, non_terminal):
        productions_for_non_terminal = []
        for production in self.productions:
            if production.start == non_terminal:
                productions_for_non_terminal.append(production)
        return productions_for_non_terminal

    def to_string(self):
        return "G = ( " + str(self.non_terminals) + ", " + str(self.terminals) + ", " + \
               str(self.productions) + str(self.starting_symbol) + " )"
