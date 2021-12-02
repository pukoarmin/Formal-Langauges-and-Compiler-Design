def head(stack):
    try:
        return stack[0]
    except:
        pass


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = {"normal_state": "normal",
                       "back_state": "back_state",
                       "final_state": "final_state",
                       "error_state": "error"}
        self.s = self.states["normal_state"]
        self.i = 1
        self.alpha = []
        self.beta = [grammar.starting_symbol]

    def __expand(self):
        pass

    def __advance(self):
        pass

    def __momentary_insuccess(self):
        pass

    def __back(self):
        pass

    def __another_try(self):
        pass

    def __success(self):
        pass

    # Descendant Recursive
    def parse(self):
        while self.s not in self.grammar.terminals and self.s != self.states["error_state"]:
            if self.s == self.states["normals_state"]:
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
            if self.s == self.states["back_state"]:
                if head(self.alpha) = "a":
                    self.__back()
                else:
                    self.__another_try()

        if self.s == self.states["error_state"]:
            print("[PARSER] -> Error")
        else:
            print("[PARSER] -> Sequence accepted")
            self.__build_string_of_production(self.alpha)