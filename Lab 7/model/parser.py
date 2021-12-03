from typing import List


def head(stack):
    try:
        return stack[0]
    except:
        pass

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    def __tree_from_derivation_seq(self, derivationString: List[str]) -> List:
        result = [(derivationString[0].split('$')[0], -1, -1)]
        i = 0
        j = 0
        while j < len(derivationString) and i < len(result):
            top = result[i]
            if top[0] not in self.grammar.N:
                i += 1
                continue
            expandWith = None
            while True:
                if '$' not in derivationString[j]:
                    j += 1
                    continue
                nonterminal, productionNumber = derivationString[j].split('$')
                if nonterminal == top[0]:
                    expandWith = (nonterminal, productionNumber)
                    break
                j += 1

            nonterminal, productionNumber = expandWith
            productionNumber = int(productionNumber)
            production = self.grammar.P[(nonterminal,)][productionNumber]
            for symbol in production:
                result.append((symbol, i, len(result) + 1))
            result[-1] = (*result[-1][:-1], -1)
            i += 1
        return result

    # Descendant Recursive
    def parse(self):
        config = ParserConfig(self.grammar)
        while config.s not in self.grammar.terminals and config.s != 'e':
            if config.s == 'q':
                if config.i == len(self.grammar.productions) and len(config.beta) == 0:
                    config.success()
                else:
                    if head(config.beta) in self.grammar.non_terminals:
                        config.expand()
                    else:
                        if head(config.beta) == "ai":
                            config.advance()
                        else:
                            config.momentary_insuccess()
            if config.s == 'b':
                if head(config.alpha) = "a":
                    config.back()
                else:
                    config.another_try()

        if config.s == 'e':
            print("[PARSER] -> Error")
        else:
            print("[PARSER] -> Sequence accepted")
            config.build_string_of_production(config.alpha)

class ParserConfig:
    def __init__(self, grammar):
        self.grammar = grammar
        self.s = 'q'
        self.i = 0
        self.alpha = []
        self.beta = []

    def expand(self):
        current = self.beta.pop()
        production = self.grammar.get_productions_for_non_terminal(current)
        if production.rules[0] != "epsilon":
            self.beta += reversed(production.rules[0])
        self.beta.append(production.rules[0] + "#0")

    def advance(self):
        self.i += 1
        terminal = self.beta.pop()
        self.alpha.append(terminal)

    def momentary_insuccess(self):
        self.s = 'b'

    def back(self):
        self.i -= 1
        terminal = self.beta.pop()
        self.alpha.append(terminal)

    def another_try(self):
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

    def success(self):
        self.s = 'f'
