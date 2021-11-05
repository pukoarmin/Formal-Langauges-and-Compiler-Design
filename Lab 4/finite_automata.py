class FiniteAutomata:
    @staticmethod
    def parse_line(line):
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].strip().split(',')]

    @staticmethod
    def parse_console(line):
        return [value.strip() for value in line.strip()[1:-1].strip().split(',')]

    @staticmethod
    def from_file(file_name):
        with open(file_name) as file:
            Q = FiniteAutomata.parse_line(file.readline())
            E = FiniteAutomata.parse_line(file.readline())
            q0 = file.readline().split('=')[1].strip()
            F = FiniteAutomata.parse_line(file.readline())

            S = FiniteAutomata.parse_transitions(FiniteAutomata.parse_line(''.join([line for line in file])))

            return FiniteAutomata(Q, E, S, q0, F)

    @staticmethod
    def from_console():
        Q = FiniteAutomata.parse_console(input('Q = '))
        E = FiniteAutomata.parse_console(input('E = '))
        q0 = input('q0 = ')
        F = FiniteAutomata.parse_console(input('F = '))

        S = FiniteAutomata.parse_transitions(FiniteAutomata.parse_console(input('S = ')))

        return FiniteAutomata(Q, E, S, q0, F)

    @staticmethod
    def parse_transitions(parts):
        result = []
        transitions = []
        index = 0

        while index < len(parts):
            transitions.append(parts[index] + ',' + parts[index + 1])
            index += 2

        for transition in transitions:
            lhs, rhs = transition.split('->')
            state2 = rhs.strip()
            state1, route = [value.strip() for value in lhs.strip()[1:-1].split(',')]

            result.append(((state1, route), state2))

        return result

    def __init__(self, Q, E, S, q0, F):
        self.Q = Q
        self.E = E
        self.S = S
        self.q0 = q0
        self.F = F

    def is_state(self, value):
        return value in self.Q

    def show_states(self):
        print(self.Q)

    def show_final_states(self):
        print(self.F)

    def show_alphabet(self):
        print(self.E)

    def get_transitions_for(self, state):
        if not self.is_state(state):
            raise Exception('Can only get transitions for states')

        return [trans for trans in self.S if trans[0][0] == state]

    def show_transitions_for(self, state):
        transitions = self.get_transitions_for(state)

        print('{ ' + ' '.join([' -> '.join([str(part) for part in trans]) for trans in transitions]) + ' }')

    def __str__(self):
        return 'Q = { ' + ', '.join(self.Q) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'F = { ' + ', '.join(self.F) + ' }\n' \
               + 'S = { ' + ', '.join([' -> '.join([str(part) for part in trans]) for trans in self.S]) + ' }\n' \
               + 'q0 = ' + str(self.q0) + '\n'
