from crossword import *
import sys


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain in self.domains:
            for word in self.domains[domain].copy():
                if len(word) != domain.length:
                    self.domains[domain].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlaps = self.crossword.overlaps[x, y]

        if overlaps:
            for word_x in self.domains[x].copy():
                y_chars = []
                x_char = word_x[overlaps[0]]
                # get all possible letters for y
                for word_y in self.domains[y]:
                    y_chars.append(word_y[overlaps[1]])
                # if x leaves no option for y, remove it
                if x_char not in y_chars:
                    self.domains[x].remove(word_x)
                    revised = True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # get arcs
        if not arcs:
            arcs = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        # while there are still inconsistent arcs
        while len(arcs) > 0:
            x, y = arcs.pop(0)
            # if domains were revised
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # add possibly affected arcs
                for z in self.crossword.neighbors(x):
                    if z is not y:
                        arcs.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for assign in assignment:
            # check unary/length constraint
            if len(assignment[assign]) != assign.length:
                return False
            # check binary/overlap constraint
            for neighbor in self.crossword.neighbors(assign):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[assign, neighbor]
                    if assignment[assign][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
        # check for distinct values
        vals = assignment.values()
        if sorted(list(set(vals))) != sorted(list(vals)):
            return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        print(var)
        print(self.domains)
        eliminated = {}
        # test each word
        for word in self.domains[var]:
            count = 0
            # test how the word affects neighbors
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    ndomain = self.domains[neighbor].copy()
                    # count how many words would be removed
                    for word_n in ndomain:
                        if word[overlap[0]] != word_n[overlap[1]]:
                            count += 1
            eliminated[word] = count
        # sort
        words = list(eliminated.keys())
        print(sorted(words, key=lambda word: eliminated[word]))
        print("-----")
        return sorted(words, key=lambda word: eliminated[word])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get all unassigned variables
        unassigned = list(self.crossword.variables - set(assignment.keys()))
        keys = {}
        # create dict of variables and their domain size and degree
        for var in unassigned:
            var_remaining = len(self.domains[var])
            var_degree = len(self.crossword.neighbors(var))
            keys[var] = (var_remaining, var_degree)
        # sort by domain size then largest degree
        return sorted(unassigned, key=lambda x: (keys[x][0], -keys[x][1]))[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # follows the given backtrack algorithm
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            temp = assignment.copy()
            temp[var] = value

            if self.consistent(temp):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
