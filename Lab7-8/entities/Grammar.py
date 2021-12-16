from typing import Set, Dict, Tuple, Iterable, List
from functools import reduce

from entities.Exceptions import not_cfg, unproductive_grammar, symbol_no_defined


class Grammar:
    def __init__(self, NonTerminals: Set[str], Terminals: Set[str],
                 Productions: Dict[Tuple[str], List[Tuple[str]]], StartingSymbol: str):
        self.non_terminals = NonTerminals
        self.terminals = Terminals
        self.productions = Productions
        self.starting_symbol = StartingSymbol
        self.CFG = True

    @staticmethod
    def production_to_string(prod: Iterable[str]) -> str:
        return reduce(lambda x, y: x + " " + y if x != "" else y, prod, "")

    @staticmethod
    def productions_to_string(productions: Tuple[Tuple[str], List[Tuple[str]]]) -> str:
        result = productions[0]
        productions_string = map(Grammar.production_to_string, productions[1])
        return Grammar.production_to_string(result) + " -> " + reduce(lambda x, y: x + " | " + y if x != "" else y,
                                                                      productions_string, "")

    def get_productions(self, non_terminal: Tuple[str]) -> List[Tuple[str]]:
        if non_terminal not in self.productions.keys():
            return list()
        return self.productions[non_terminal]

    @staticmethod
    def remove_left_recursion(grammar: 'Grammar') -> 'Grammar':
        if not grammar.CFG:
            raise not_cfg
        new_grammar = Grammar(grammar.non_terminals.copy(), grammar.terminals.copy(), grammar.productions.copy(),
                              grammar.starting_symbol)
        predicate = lambda rhs, lhs: rhs[0] == lhs
        LHSs = list(new_grammar.productions.keys())
        for i, LHS in enumerate(LHSs):
            changed = True
            while changed:
                changed = False
                RHS = set(new_grammar.productions[LHS])
                new_rhs = set()
                for alphai in RHS:
                    leadingSymbol = alphai[0]
                    if leadingSymbol not in new_grammar.non_terminals or (leadingSymbol,) not in LHSs[:i]:
                        new_rhs.add(alphai)
                        continue
                    betai = alphai[1:]
                    for alphaj in new_grammar.productions[(leadingSymbol,)]:
                        new_rhs.add(alphaj + betai)
                if new_rhs != RHS:
                    changed = True
                new_grammar.productions[LHS] = list(new_rhs)

            RHS = new_grammar.productions[LHS][:]
            new_rhs = []
            recursive_rhs_indices = [i for i, e in enumerate(RHS) if predicate(e, LHS[0])]
            non_recursive_rhs_indices = [i for i, e in enumerate(RHS) if not predicate(e, LHS[0])]
            if len(recursive_rhs_indices) > 0 and len(non_recursive_rhs_indices) > 0:
                new_symbol = LHS[0] + "'"
                new_grammar.non_terminals.add(new_symbol)
                new_symbol = (new_symbol,)
                for index in non_recursive_rhs_indices:
                    new_production = RHS[index] + new_symbol
                    new_rhs.append(new_production)

                new_productions = {('epsilon',)}
                for index in recursive_rhs_indices:
                    new_production = RHS[index][1:] + new_symbol
                    new_productions.add(new_production)
                new_grammar.productions[new_symbol] = list(new_productions)
            elif len(recursive_rhs_indices) > 0 and len(non_recursive_rhs_indices) == 0:
                raise unproductive_grammar()
            else:
                new_rhs = RHS.copy()

            new_grammar.productions[LHS] = list(new_rhs)

        return new_grammar

    @staticmethod
    def read_from_file(filename: str) -> 'Grammar':
        grammar = Grammar(set(), set(), {}, "")
        with open(filename, "r") as f:
            grammar.starting_symbol = f.readline().split()[0]
            grammar.non_terminals.add(grammar.starting_symbol)
            for non_terminal in f.readline().split():
                grammar.non_terminals.add(non_terminal)

            for terminal in f.readline().split():
                grammar.terminals.add(terminal)

            for line in f:
                production = line.split()
                i = 0
                key = []
                while production[i] != "->":
                    if production[i] not in grammar.terminals and production[i] not in grammar.non_terminals:
                        raise symbol_no_defined(production)
                    key.append(production[i])
                    i += 1

                if len(key) > 1:
                    grammar.CFG = False

                prod = []
                productions = set()
                for entry in production[i + 1:]:
                    if entry == "|":
                        productions.add(tuple(prod))
                        prod = []
                        continue
                    if entry not in grammar.terminals and entry not in grammar.non_terminals and entry != "epsilon":
                        raise symbol_no_defined(entry)
                    prod.append(entry)
                productions.add(tuple(prod))
                grammar.productions[tuple(key)] = list(productions)

        return grammar
