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
                        token = token.strip()
                        if line_index == 0:
                            self.non_terminals.append(token)
                        if line_index == 1:
                            self.terminals.append(token)
                        if line_index == 2:
                            self.starting_symbol = token
                if line_index > 2:
                    tokens = line.split(" -> ")
                    rules = []
                    for rule in tokens[1].split(" | "):
                        rules.append(rule.split())
                    production = Production(tokens[0], rules)
                    self.productions.append(production)

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

    def CFG_check(self):
        for production in self.productions:
            for elem in production.rules:
                for e in elem:
                    if e == 'epsilon' or e in self.terminals or e in self.non_terminals:
                        continue
                    else:
                        return False
        return True

    def to_string(self):
        production_string = ""
        for production in self.productions:
            production_string += str(production)
        return "G = ( " + str(self.non_terminals) + ", " + str(self.terminals) + ", " + \
               str(production_string) + str(self.starting_symbol) + " )"
