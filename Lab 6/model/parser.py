def head(stack):
    try:
        return stack[0]
    except:
        pass

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

class ParserConfig:
    def __init__(self, grammar):
        self.grammar = grammar
        self.s = 'q'
        self.i = 0
        self.alpha = []
        self.beta = []

    def __expand(self):
        current = self.beta.pop()
        production = self.grammar.get_productions_for_non_terminal(current)
        if production.rules[0] != "epsilon":
            self.beta += reversed(production.rules[0])
        self.beta.append(production.rules[0] + "#0")

    def __advance(self):
        self.i += 1
        terminal = self.beta.pop()
        self.alpha.append(terminal)

    def __momentary_insuccess(self):
        self.s = 'b'

    def __back(self):
        self.i -= 1
        terminal = self.beta.pop()
        self.alpha.append(terminal)

    def __another_try(self):
        symbl = self.alpha.pop()
        non_terminal, production_nbr = symbl.split("#")
        production_nbr = int(production_nbr)
        productions = self.grammar.get_productions_for_non_terminal(non_terminal)

        current_production = productions[production_nbr]
        for el in current_production:
            el = self.beta.pop()

        if production_nbr < len(productions) - 1:
            new_production = productions[production_nbr + 1]
            if new_production != "epsilon":
                self.beta += reversed(new_production)
            self.beta.append(non_terminal + "#{0}".format(production_nbr + 1))
            self.s = 'q'
            return

        if self.i == 0 and non_terminal == self.grammar.S:
            self.s = 'e'
            return
        self.beta.append(non_terminal)

    def __success(self):
        self.s = 'f'

    # Descendant Recursive
    def parse(self):
        while self.s not in self.grammar.terminals and self.s != 'e':
            if self.s == 'q':
                if self.i == len(self.grammar.productions) and len(self.beta) == 0:
                    self.__success()
                else:
                    if head(self.beta) in self.grammar.non_terminals:
                        self.__expand()
                    else:
                        if head(self.beta) == "ai":
                            self.__advance()
                        else:
                            self.__momentary_insuccess()
            if self.s == 'b':
                if head(self.alpha) = "a":
                    self.__back()
                else:
                    self.__another_try()

        if self.s == 'e':
            print("[PARSER] -> Error")
        else:
            print("[PARSER] -> Sequence accepted")
            self.__build_string_of_production(self.alpha)