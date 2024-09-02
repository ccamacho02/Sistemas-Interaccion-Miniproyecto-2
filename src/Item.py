class Item:
    def __init__(self, name, description, action=""):
        self.name = name  # Name of the item
        self.description = description  # Description of the item
        self.action = action
    
    def describe(self):
        """
        Prints the description of the item.
        """
        print(f"{self.name}: {self.description}")

    def use(self):
        """
        Defines how the item is used by the character.
        Can be overridden by subclasses for specific behaviors.
        :param character: The character using the item.
        """
        print(f"Usando... {self.name}\n{self.action}")