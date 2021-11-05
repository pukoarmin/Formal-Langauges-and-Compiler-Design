from finite_automata import FiniteAutomata

if __name__ == '__main__':
    # ==== Finite Automata ====
    # Read the Finite Automata from the file
    finite_automata = FiniteAutomata.from_file('fa.in')
    print("\n==== Finite Automata ====")
    print(finite_automata)

    # Print states
    print("==== States ===")
    finite_automata.show_states()

    # Print alphabet
    print("\n === Alphabet ===")
    finite_automata.show_alphabet()

    # Print final states
    print("\n === Final States")
    finite_automata.show_final_states()

    # Print the transitions for a given state
    try:
        state = "q1"
        print("\n==== Transition for " + state + " ====")
        finite_automata.show_transitions_for(state)
    except Exception as e:
        print(e)

    # Read the Finite Automata from console
    # finiteAutomata2 = FiniteAutomata.fromConsole()
    # print('\n' + str(finiteAutomata2))
