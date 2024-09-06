class Puzzle:
    def __init__(self, description, solution):
        """
        Initializes a puzzle with a description and a solution.
        :param description: A brief description of the puzzle.
        :param solution: The correct solution to the puzzle.
        """
        self.description = description  # Description of the puzzle
        self.solution = solution.lower()  # The correct solution to the puzzle (stored in lowercase)

    def show(self):
        """
        Displays the description of the puzzle to the player.
        """
        print(f"Puzzle: {self.description}")

    def attempt(self, player_solution):
        """
        Checks if the player's solution is correct.
        :param player_solution: The player's proposed solution to the puzzle.
        :return: True if the solution is correct, False otherwise.
        """
        return player_solution.strip().lower() == self.solution
