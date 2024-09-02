class Room:
    def __init__(self, name, description, scene="", visited=False):
        self.name = name 
        self.description = description  
        self.items = []  
        self.connections = {}
        self.visited = visited
        self.scene = scene

    def describe(self):
        print(f"{self.name}: {self.description}")

    def connect(self, direction, room):
        self.connections[direction] = room

    def look_around(self):
        if self.items:
            print(f"Objetos en la habitación: {', '.join(item.name for item in self.items)}")
        else:
            print("No hay objetos aquí.")

    def get_room_in_direction(self, direction):
        return self.connections.get(direction)

    def add_item(self, items):
        for item in items:
            self.items.append(item)

    # def remove_item(self, item):
    #     if item in self.items:
    #         self.items.remove(item)
    #     else:
    #         print(f"{item.name} no está en la habitación.")
    
    def mark_as_visited(self):
        self.visited = True

    def start_scene(self):
        print(self.scene)