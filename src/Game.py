import os
import random

from Entities import Character, Enemy
from Room import Room
from Item import Item
from Puzzle import Puzzle
from Dialogue import Dialogue
from Audio_manager import Sound

class Game:
    def __init__(self):
        self.sacred_objects = self.setup_sacred_objects()
        self.objects = self.setup_objects()
        self.player = self.create_player()
        self.room_name_map = self.create_room_name_map()
        self.sounds = self.setup_sounds()
        self.sacred_objects_collected = 0
        self.solved_puzzles = 0
        self.story_events = self.setup_story_events()
        self.puzzles = self.setup_puzzles()
        self.dialogues = self.setup_dialogues()
        self.enemies = self.setup_enemies()
        self.story_events = self.setup_story_events()
        self.rooms = self.create_rooms()
        self.current_room = self.rooms['forest_entrance']

    def create_player(self):
        return Character("El explorador", "Valiente aventurero perdido en el bosque encantado.")
    
    def create_rooms(self):
        forest_entrance = Room("Entrada del Bosque", "Estás en la entrada del bosque encantado. Hay una neblina espesa.", "Te despiertas al pie de un árbol antiguo...")
        clearing = Room("Claro del Bosque", "Un pequeño claro donde apenas penetra la luz de la luna entre las copas de los árboles.")
        dark_cave = Room("Cueva Oscura", "Una cueva oscura y húmeda donde escuchas el eco de un lobo a lo lejos.")
        whispering_tree = Room("Árbol de los Susurros", "Un árbol antiguo que susurra en un idioma olvidado.")
        black_lake = Room("Lago Negro", "Un lago oscuro y siniestro, en el centro se encuentra una isla con un árbol dorado.")
        stone_altar = Room("Altar de Piedra", "Un pequeño altar al pie de una colina, donde descansa una campana de plata.")

        forest_entrance.connect('norte', clearing)
        clearing.connect('sur', forest_entrance)
        clearing.connect('este', dark_cave)
        dark_cave.connect('oeste', clearing)
        clearing.connect('norte', whispering_tree)
        whispering_tree.connect('sur', clearing)
        whispering_tree.connect('este', black_lake)
        black_lake.connect('oeste', whispering_tree)
        black_lake.connect('norte', stone_altar)
        stone_altar.connect('sur', black_lake)

        

        forest_entrance.add_item(self.objects["Entrada del Bosque"])

        return {
            'forest_entrance': forest_entrance,
            'clearing': clearing,
            'dark_cave': dark_cave,
            'whispering_tree': whispering_tree,
            'black_lake': black_lake,
            'stone_altar': stone_altar
        }
    
    def create_room_name_map(self):
        return {
            "entrada_del_bosque": "forest_entrance",
            "claro_del_bosque": "clearing",
            "cueva_oscura": "dark_cave",
            "árbol_de_los_susurros": "whispering_tree",
            "lago_negro": "black_lake",
            "altar_de_piedra": "stone_altar"
        }
    
    def setup_objects(self):
        old_map = Item("Mapa", "Un viejo mapa del bosque con rutas y notas de exploradores anteriores.", "El mapa muestra varios puntos de interés en el bosque...")
        oil_lamp = Item("Lampara de Aceite", "Una lámpara de aceite medio llena, ideal para iluminar lugares oscuros.", "Los enemigos de la habitacion se revelan...")
        antique_scroll = Item("Pergamino Antiguo", "Un pergamino escrito con runas misteriosas que podrían contener un hechizo.")

        return {
            "Entrada del Bosque": [old_map, oil_lamp],
            "Claro del Bosque": [antique_scroll]
        }



    def setup_sacred_objects(self):
        """
        Sets up the sacred objects required to complete the game.
        :return: A dictionary of sacred objects.
        """
        feather = Item("Pluma Dorada", "Una pluma dorada brillante, parece tener un poder especial.")
        bell = Item("Campana de Plata", "Una campana de plata antigua, con grabados místicos en su superficie.")

        return {
            "Enemigo Cueva": [feather],
            "Enemigo Lago": [bell]
        }
    
    def setup_sounds(self):
        base_path = os.path.dirname(__file__)  # Get the directory where game.py is located
        project_root = os.path.abspath(os.path.join(base_path, os.pardir))  # Move up to the project root
        audio_path = os.path.join(project_root, 'audio')
        sounds = {
            'forest_entrance': Sound(os.path.join(audio_path, "forest_entrance.wav"), position='center'),
        }

        return sounds
    
    def setup_story_events(self):
        """
        Sets up the story events to be displayed at different points in the game.
        :return: A list of story events.
        """
        return [
            "Encuentras un pergamino antiguo con runas que no entiendes...",
            "Sigues una sombra hasta un árbol que parece respirar...",
            "Te diriges hacia la cueva oscura, donde un espíritu emerge...",
            "Resuelves tres acertijos del espíritu y obtienes un fragmento de cristal...",
            "Te diriges al Lago Negro y construyes una balsa para cruzar...",
            "Llegas al Altar de Piedra y encuentras la campana de plata...",
        ]
    
    def setup_puzzles(self):
        """
        Sets up the puzzles for different locations in the game.
        :return: A dictionary of puzzles mapped to their corresponding room names.
        """
        cave_puzzle = Puzzle(
            "Para obtener el fragmento de cristal, resuelve esto: 'Soy algo que siempre está delante de ti pero nunca podrás ver.'",
            "el futuro"
        )
        lake_puzzle = Puzzle(
            "Para cruzar el lago, debes responder: 'Mientras más seco estoy, más húmedo estoy. ¿Qué soy?'",
            "una toalla"
        )
        altar_puzzle = Puzzle(
            "Para obtener la campana de plata, responde: 'No puedes tocarme aunque me veas. ¿Quién soy?'",
            "una sombra"
        )

        return {
            "Cueva Oscura": cave_puzzle,
            "Lago Negro": lake_puzzle,
            "Altar de Piedra": altar_puzzle
        }
    
    def solve_puzzle(self):
        """
        Allows the player to solve a puzzle in the current room.
        """
        if self.current_room.name in self.puzzles:
            puzzle = self.puzzles[self.current_room.name]
            puzzle.show()
            player_solution = input("Tu respuesta: ")
            if puzzle.attempt(player_solution):
                print("¡Correcto! Has resuelto el acertijo.")
                self.solved_puzzles += 1
                self.puzzles.pop(self.current_room.name)
                if self.solved_puzzles == 3:
                    fragment = Item("Fragmento de Cristal", "Un fragmento brillante que parece emitir una luz etérea.")
                    self.player.add_to_inventory([fragment])
                    self.objective([fragment])
                    print("Lo lograste, has obtenido el fragmento de cristal")
            else:
                print("Incorrecto. Inténtalo de nuevo.")
        else:
            print("No hay acertijos aquí.")

    def setup_dialogues(self):
        """
        Sets up the dialogues for different locations in the game.
        :return: A dictionary of dialogues mapped to their corresponding room names or events.
        """
        tree_dialogue = Dialogue([
            "El Árbol de los Susurros dice: 'Este bosque solía ser un lugar de paz...'",
            "'Pero una maldición ha caído sobre nosotros. Para escapar, debes encontrar tres objetos sagrados...'",
            "'Un fragmento de cristal, una pluma dorada, y una campana de plata. Están ocultos y protegidos.'"
        ])

        guardian_dialogue = Dialogue([
            "El Guardián encapuchado dice: 'Has llegado lejos, pero el puente requiere un precio para cruzar.'",
            "'Entrega los tres objetos sagrados y no mires atrás mientras cruzas.'",
            "'Si te atreves a mirar atrás, quedarás atrapado para siempre...'"
        ])

        return {
            "Árbol de los Susurros": tree_dialogue,
            "Guardían del Puente": guardian_dialogue
        }
    
    def setup_enemies(self):
        """
        Configura los enemigos en diferentes ubicaciones del juego.
        :return: Un diccionario de enemigos mapeados a sus nombres de habitación correspondientes.
        """
        cave_enemy = Enemy("Espíritu Malévolo", "Un espíritu con ojos brillantes y una sonrisa malévola.", health=50, attack_power=15, inventory=self.sacred_objects["Enemigo Cueva"])
        lake_enemy = Enemy("Serpiente del Lago", "Una serpiente gigante que emerge del lago oscuro.", health=80, attack_power=20, inventory=self.sacred_objects["Enemigo Lago"])

        return {
            "Cueva Oscura": cave_enemy,
            "Lago Negro": lake_enemy
        }

    def play_dialogue(self):
        """
        Plays a dialogue in the current room or event.
        """
        if self.current_room.name in self.dialogues:
            dialogue = self.dialogues[self.current_room.name]
            while not dialogue.is_finished():
                dialogue.show_next_line()
                input("(Presiona Enter para continuar...)")
        else:
            print("No hay nadie con quien hablar aquí.")

    def fight_enemy(self):
        if self.current_room.name in self.enemies:
            enemy = self.enemies[self.current_room.name]
            while enemy.is_alive() and self.player.is_alive():
                print(f"¡Un {enemy.name} ha aparecido!")
                action = input("¿Quieres 'atacar' o 'huir'? ").strip().lower()
                if action == 'atacar':
                    enemy.attack(self.player)
                    if self.player.is_alive():
                        print(f"Atacas a {enemy.name} y le causas 10 de daño.")
                        enemy.take_damage(10)
                    if not enemy.is_alive():
                        print(f"¡Has derrotado a {enemy.name}!")
                elif action == 'huir':
                    print("Huyes de la pelea.")
                    break
                else:
                    print("Acción no válida.")
        else:
            print("No hay enemigos aquí.")

    def play(self):
        print("Bienvenido al bosque encantado!")
        self.play_sound_for_current_room()
        self.current_room.describe()
        self.current_room.mark_as_visited()
        self.display_story_event(self.sacred_objects_collected)
        try:
            while self.player.is_alive():
                command = input("> ").strip().lower()
                self.handle_commands(command)
        finally:
            self.cleanup()

    def handle_commands(self,command):
        if command in ["norte", "sur", "este", "oeste"]:
            self.move_player(command)
        elif command == "ver":
            self.current_room.look_around()
        elif command == "hablar":
            self.play_dialogue()
        elif command.startswith("usar "):
            item = int(command.split(" ")[1])
            self.use_item(item)
        elif command == "inventario":
            self.player.show_inventory()
        elif command == "recoger":
            self.collect_object()
        elif command == "resolver":
            self.solve_puzzle()
        elif command == "pelear":
            self.fight_enemy()
        elif command == "salir":
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            exit(1)
        else:
            print("No entiendo ese comando.")
    
    def play_sound_for_current_room(self):
        room_key = self.current_room.name.lower().replace(" ", "_")
        if room_key in self.room_name_map:
            sound_key = self.room_name_map[room_key]
            if sound_key in self.sounds:
                sound = self.sounds[sound_key]
                sound.play()

    def use_item(self, item):
        if  0 < item and item <= len(self.player.inventory):
            object = self.player.inventory[item-1]
            object.use()
            if object.name == "Lampara de Aceite":
                self.show_enemies()
        else: 
            print("Seleccione un objeto de su inventario")

    def show_enemies(self):
        try:
            enemy = self.enemies[self.current_room.name]
            if enemy.is_alive():
                enemy.describe()
                enemy.attack(self.player)
                self.fight_enemy(enemy)
            else:
                print("Ya has derrotado a los enemigos de esta habitacion!")
        except KeyError:
            print("No hay enemigos aqui!")

    def fight_enemy(self, enemy):
        while enemy.is_alive() and self.player.is_alive():
            print(f"\nTu salud: {self.player.health} | Salud de {enemy.name}: {enemy.health}")
            action = input("¿Qué deseas hacer? ('atacar', 'defender', 'huir'):> ").strip().lower()

            if action == 'atacar':
                print(f"Atacas a {enemy.name} y le causas 10 de daño.")
                enemy.take_damage(100)

                if enemy.is_alive():
                    print(f"{enemy.name} contraataca!")
                    enemy.attack(self.player)
            
            elif action == 'defender':
                print("Te preparas para defenderte del próximo ataque.")
                damage_taken = max(0, enemy.attack_power - 5)  
                print(f"{enemy.name} te ataca, pero reduces el daño a {damage_taken}!")
                self.player.take_damage(damage_taken)

            elif action == 'huir':
                escape_chance = random.random()  
                if escape_chance > 0.5:  
                    print("Logras escapar del combate y esconderte")
                    self.current_room.describe()
                    return  
                else:
                    print("Intentas huir, pero el enemigo te bloquea el camino y te ataca!")
                    enemy.attack(self.player)

            else:
                print("Acción no válida. Por favor, elige 'atacar', 'defender' o 'huir'.")

            if not self.player.is_alive():
                print("Has sido derrotado... ¡Juego terminado!")
                exit(1)  

            if not enemy.is_alive():
                print(f"¡Has derrotado a {enemy.name}! y has recuperado tu salud")
                items = enemy.inventory
                self.player.add_to_inventory(items)
                self.objective(items)
                self.player.health = 100
                self.current_room.describe()

    def objective(self, items):
        self.sacred_objects_collected += 1
        print(f"Has encontrado un {', '.join(item.name for item in items)}. Objetos sagrados recolectados: {self.sacred_objects_collected}/3.")
        if self.sacred_objects_collected == 3:
            print("¡Has recolectado los tres objetos sagrados! Regresa al puente roto para escapar.")

    def move_player(self, direction):
        """
        Moves the player in a specified direction.
        :param direction: The direction the player wants to move.
        """
        next_room = self.current_room.get_room_in_direction(direction)

        if not next_room:
            print("No puedes ir en esa dirección.")
            return

        try:
            enemy = self.enemies[self.current_room.name]
            if enemy.is_alive() and not self.current_room.visited:
                print("No puedes ir en esa dirección. Aún hay cosas por explorar")
                return
        except KeyError:
            pass
        print("Decides seguir el sendero, tus pasos crujen sobre las hojas secas...")
        self.current_room.mark_as_visited()
        self.current_room = next_room
        self.current_room.describe()
        self.play_sound_for_current_room()
        self.display_story_event(self.sacred_objects_collected + 1)

    def collect_object(self):
        """
        Collects a sacred object in the current room, if available.
        """
        if self.current_room.name not in self.sacred_objects and self.current_room.name not in self.objects:
            print("No hay objetos que recolectar aquí.")
        else:
            if self.current_room.name in self.objects:
                items = self.objects[self.current_room.name]
                self.player.add_to_inventory(items)
                print(f"Has encontrado un {', '.join(item.name for item in items)}.")

    def display_story_event(self, index):
        """
        Displays a part of the story based on the index.
        :param index: The index of the story event to display.
        """
        if index < len(self.story_events):
            print(self.story_events[index])
    
    def cleanup(self):
        for sound in self.sounds.values():
            sound.cleanup()

if __name__ == "__main__":
    game = Game()
    game.play()
