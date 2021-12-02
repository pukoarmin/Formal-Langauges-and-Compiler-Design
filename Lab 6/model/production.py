class Production:
    def __init__(self, start, rules):
        self.start = start
        self.rules = rules

    def __str__(self):
        built_string = self.start + " -> "
        for rule_set in self.rules:
            for rule in rule_set:
                built_string = built_string + rule + " "
        built_string += "\n"
        return built_string
