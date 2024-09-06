class Dialogue:
    def __init__(self, lines):
        """
        Initializes a dialogue with a list of lines.
        :param lines: A list of dialogue lines.
        """
        self.lines = lines  # List of lines in the dialogue
        self.current_line = 0  # Tracks the current line being displayed

    def start(self):
        """
        Starts the dialogue, displaying it line by line.
        """
        print("Inicio de dialogo...")
        self.show_next_line()

    def show_next_line(self):
        """
        Displays the next line in the dialogue.
        """
        if self.current_line < len(self.lines):
            print(self.lines[self.current_line])
            self.current_line += 1
        else:
            print("Dialogo finalizado.")
    
    def is_finished(self):
        """
        Checks if the dialogue has finished.
        :return: True if the dialogue is finished, False otherwise.
        """
        return self.current_line >= len(self.lines)
    
    def reset(self):
        """
        Resets the dialogue to the beginning.
        """
        self.current_line = 0
