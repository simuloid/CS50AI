import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safe = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __repr__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        self.check_mines()
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        self.check_safes()
        return self.safe

    def check_safes(self):
        """
        Checks to see if count is 0, and if so, marks all remaining
        cells as safe.

        Returns
        -------
        None.

        """
        if 0 == self.count:
            for c in self.cells.copy():
                self.mark_safe(c)
                
    def check_mines(self):
        """
        Checks to see if count == len(cells), and if so, marks all remaining
        cells as mines.

        Returns
        -------
        None.

        """
        if len(self.cells) == self.count:
            for c in self.cells.copy():
                self.mark_mine(c)
                
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mines.add(cell)
            self.cells.remove(cell)
            self.count -= 1
            self.check_safes()

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safe.add(cell)
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def neighbors(self, cell):
        rc = set()
        for r in range(cell[0]-1, cell[0]+2):
            for c in range(cell[1]-1, cell[1]+2):
                if r >= 0 and r < self.height and c >= 0 and c < self.width:
                    n = (r,c)
                    if not n in self.moves_made and not n in self.safes and not n in self.mines:
                        rc.add((r,c))

        return rc

    def infer_safes(self):
        to_remove = []
        for s in self.knowledge:
            if s.count == 0:
                to_remove.append(s)
                for c in s.cells.copy():
                    self.mark_safe(c)
                
    def infer_mines(self):
        to_remove = []
        for s in self.knowledge:
            if s.count == len(s.cells):
                to_remove.append(s)
                for c in s.cells.copy():
                    self.mark_mine(c)
                
    def cleanup_knowledge(self):
        to_remove = []
        for s in self.knowledge:
            if not s.cells:
                assert not s.count
                to_remove.append(s)
        for r in to_remove:
            self.knowledge.remove(r)
            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        group = self.neighbors(cell)
        s = Sentence(group, count)
        self.knowledge.append(s)
#        self.infer_safes()
#        self.infer_mines()
        new_knowledge = []
        for s in self.knowledge:
            for t in self.knowledge:
                if s == t:
                    continue
                if s.cells.issubset(t.cells):
                    set_diff = t.cells - s.cells
                    count_diff = t.count - s.count
                    if set_diff:
                        new_knowledge.append(Sentence(set_diff, count_diff))
        self.knowledge.extend(new_knowledge)
        self.infer_safes()
        self.infer_mines()
        self.cleanup_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        choices = self.safes - self.moves_made
        if choices:
            return random.choice(list(choices))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        choices = set([(i,j) for i in range(self.height) for j in range(self.width)])
        choices = choices - self.moves_made
        choices = choices - self.mines
        if choices:
            return random.choice(list(choices))
        return None
