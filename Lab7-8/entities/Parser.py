from typing import Tuple, List
import pydot

from entities.Grammar import Grammar


class RDParser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def parse(self, word: Tuple) -> 'ParserOutput':
        config = RDConfig(self.grammar)
        while config.state_of_parsing not in {'f', 'e'}:
            if config.state_of_parsing == 'q':
                if config.position_of_current_symbol == len(word) and len(config.input_stack) == 0:
                    config.success()
                else:
                    if len(config.input_stack) > 0 and config.input_stack[-1] in self.grammar.non_terminals:
                        config.expand()
                    else:
                        if config.position_of_current_symbol < len(word) and len(config.input_stack) > 0 and \
                                config.input_stack[-1] == word[config.position_of_current_symbol]:
                            config.advance()
                        else:
                            config.momentary_insuccess()
            else:
                if config.state_of_parsing == 'b':
                    if len(config.working_stack) > 0 and config.working_stack[-1] in self.grammar.terminals:
                        config.back()
                    elif len(config.working_stack) > 0:
                        config.another_try()

        if config.state_of_parsing == 'e':
            print('[PARSER] - error')
            return ParserOutput(self.grammar, [])
        print('[PARSER] - sequence accepted')
        return ParserOutput(self.grammar, config.working_stack)


class ParserOutput:
    def __init__(self, grammar, production_string):
        self.tree = self.get_tree(grammar, production_string)
        self.grammar = grammar
        self.production_string = production_string

    @staticmethod
    def get_tree(grammar, production_string):
        if not production_string:
            return []
        result = [(production_string[0].split('$')[0], -1, -1)]
        i = 0
        j = 0
        while j < len(production_string) and i < len(result):
            top = result[i]
            if top[0] not in grammar.non_terminals:
                i += 1
                continue
            expand_with = None
            while True:
                if '$' not in production_string[j]:
                    j += 1
                    continue
                non_terminal, production_number = production_string[j].split('$')
                if non_terminal == top[0]:
                    expand_with = (non_terminal, production_number)
                    j += 1
                    break
                j += 1

            non_terminal, production_number = expand_with
            production_number = int(production_number)
            production = grammar.productions[(non_terminal,)][production_number]
            added = 1
            for symbol in production:
                result.insert(i + added, (symbol, i, i + 1 + added))
                added += 1
            result[i + added - 1] = (*result[i + added - 1][:-1], -1)
            i += 1
        return result

    def plot_parse_tree(self, filename="some_graph.png"):
        digraph = pydot.Dot("some_graph", graph_type="digraph")
        nodes = []
        for i in range(len(self.tree)):
            idx_as_str = str(i)
            elem = self.tree[i]
            node = pydot.Node(idx_as_str, label='"' + elem[0] + '"')
            digraph.add_node(node)
            nodes.append(node)
            if elem[1] != -1:
                edge = pydot.Edge(str(elem[1]), idx_as_str)
                digraph.add_edge(edge)
        digraph.write(filename, format="png")


class RDConfig:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.state_of_parsing = 'q'
        self.position_of_current_symbol = 0
        self.working_stack: List[str] = []
        self.input_stack: List[str] = [grammar.starting_symbol]

    def expand(self):
        current_symbol = self.input_stack.pop()
        production = self.grammar.get_productions((current_symbol,))
        if production[0] != ('epsilon', ):
            self.input_stack += reversed(production[0])
        self.working_stack.append(current_symbol + "$0")

    def advance(self):
        self.position_of_current_symbol += 1
        terminal = self.input_stack.pop()
        self.working_stack.append(terminal)

    def momentary_insuccess(self):
        self.state_of_parsing = 'b'

    def back(self):
        self.position_of_current_symbol -= 1
        terminal = self.working_stack.pop()
        self.input_stack.append(terminal)

    def another_try(self):
        annotated_symbol = self.working_stack.pop()
        non_terminal, production_number = annotated_symbol.split("$")
        production_number = int(production_number)
        productions = self.grammar.get_productions((non_terminal,))

        current_production = productions[production_number]
        for production in current_production:
            if production != "epsilon":
                _ = self.input_stack.pop()

        if production_number < len(productions) - 1:
            new_production = productions[production_number + 1]
            if new_production != ('epsilon', ):
                self.input_stack += reversed(new_production)
            self.working_stack.append(non_terminal + "${0}".format(production_number + 1))
            self.state_of_parsing = 'q'
            return

        if self.position_of_current_symbol == 0 and non_terminal == self.grammar.starting_symbol:
            self.state_of_parsing = 'e'
            return

        self.input_stack.append(non_terminal)

    def success(self):
        self.state_of_parsing = 'f'
