class Character:
    def __init__(self, name, description, health=100, inventory=None):

        self.name = name  
        self.description = description  
        self.health = health  
        self.inventory = inventory if inventory is not None else [] 

    def describe(self):
        print(f"{self.name}: {self.description}")

    def is_alive(self):

        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print(f"{self.name} ha muerto.")

    def heal(self):
        print(self.health)

    def add_to_inventory(self, items):
        for item in items:
            self.inventory.append(item)
            print(f"{item.name} ha sido añadido a tu inventario.")

    def remove_from_inventory(self, item):

        if item in self.inventory:
            self.inventory.remove(item)

    def show_inventory(self):

        if self.inventory:
            print(f"Inventario de {self.name}:") 
            for i in range(len(self.inventory)):
                print(f"{i+1}) {self.inventory[i].name}")
        else:
            print(f"{self.name} no tiene objetos en el inventario.")

class Enemy(Character):
    def __init__(self, name, description, health, attack_power, inventory):
        super().__init__(name, description, health, inventory)
        self.attack_power = attack_power

    def attack(self, target):
        print(f"{self.name} ataca a {target.name} causando {self.attack_power} de daño!")
        target.take_damage(self.attack_power)
