from entities.Grammar import Grammar
from entities.Parser import RDParser


def get_program():
    program = []
    with open("resources/seq.txt", "r") as f:
        for line in f:
            if line != "":
                program.append(line.strip())
    return tuple(program)


if __name__ == '__main__':
    grmr = Grammar.read_from_file("resources/g1.txt")
    grmr = Grammar.remove_left_recursion(grmr)
    parser = RDParser(grmr)

    prg = get_program()
    result = parser.parse(prg).plot_parse_tree("output/g1_output.png")
