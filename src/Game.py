import os
import random

from Entities import Character, Enemy
from Room import Room
from Item import Item
from Puzzle import Puzzle
from Dialogue import Dialogue
from Audio_manager import Sound
from sounds import SOUNDS
from time import sleep


class Game:
    def __init__(self):
        self.sacred_objects_list = []
        self.sacred_objects = self.setup_sacred_objects()
        self.objects = self.setup_objects()
        self.player = self.create_player()
        self.room_name_map = self.create_room_name_map()
        self.sacred_objects_collected = 0
        self.solved_puzzles = 0
        self.puzzles = self.setup_puzzles()
        self.dialogues = self.setup_dialogues()
        self.enemies = self.setup_enemies()
        self.rooms = self.create_rooms()
        self.current_room = self.rooms['forest_entrance']
        self.audio_path = self.setup_sounds()
        self.sound = None

    def create_player(self):
        return Character("El explorador", "Valiente aventurero perdido en el bosque encantado.")

    def create_rooms(self):
        forest_entrance = Room("Entrada del Bosque", "Estás en la entrada del bosque encantado. Hay una neblina espesa.",
                               "Te despiertas al pie de un árbol antiguo...")
        clearing = Room(
            "Claro del Bosque", "Un pequeño claro donde apenas penetra la luz de la luna entre las copas de los árboles.")
        dark_cave = Room(
            "Cueva Oscura", "Una cueva oscura y húmeda donde escuchas el eco de un lobo a lo lejos.", "Un espíritu emerge de la oscuridad...", character='espiritu')
        whispering_tree = Room(
            "Árbol de los Susurros", "Un árbol antiguo que susurra en un idioma olvidado.", "El árbol te habla...", character='arbol')
        black_lake = Room(
            "Lago Negro", "Un lago oscuro y siniestro, en el centro se encuentra una isla con un árbol dorado.", "Encuentras madera y construyes una balsa para cruzar.", character='balsa')
        stone_altar = Room(
            "Altar de Piedra", "Un pequeño altar al pie de una colina, donde descansa una campana de plata.")
        broken_bridge = Room("Puente Roto", "Puente antiguo que dirige a la salida del bosque.")


        forest_entrance.connect('norte', clearing)
        clearing.connect('sur', forest_entrance)
        clearing.connect('este', dark_cave)
        dark_cave.connect('oeste', clearing)
        clearing.connect('norte', whispering_tree)
        whispering_tree.connect('sur', clearing)
        whispering_tree.connect('este', black_lake)
        black_lake.connect('oeste', whispering_tree)
        black_lake.connect('norte', stone_altar)
        black_lake.connect('este', broken_bridge)
        broken_bridge.connect("oeste", black_lake)
        stone_altar.connect('sur', black_lake)

        forest_entrance.add_item(self.objects["Entrada del Bosque"])

        return {
            'forest_entrance': forest_entrance,
            'clearing': clearing,
            'dark_cave': dark_cave,
            'whispering_tree': whispering_tree,
            'black_lake': black_lake,
            'broken_bridge': broken_bridge,
            'stone_altar': stone_altar,
        }

    def create_room_name_map(self):
        return {
            "entrada_del_bosque": "forest_entrance",
            "claro_del_bosque": "clearing",
            "cueva_oscura": "dark_cave",
            "árbol_de_los_susurros": "whispering_tree",
            "lago_negro": "black_lake",
            "puente_roto": "broken_bridge",
            "altar_de_piedra": "stone_altar",
        }

    def setup_objects(self):
        old_map = Item("Mapa", "Un viejo mapa del bosque con rutas y notas de exploradores anteriores.",
                       "El mapa muestra varios puntos de interés en el bosque...")
        oil_lamp = Item("Lampara de Aceite", "Una lámpara de aceite medio llena, ideal para iluminar lugares oscuros.",
                        "Los enemigos de la habitacion se revelan...")
        antique_scroll = Item(
            "Pergamino Antiguo", "Un pergamino escrito con runas misteriosas que podrían contener un hechizo.", "Tu salud se ha regenerado")
        

        return {
            "Entrada del Bosque": [old_map, oil_lamp],
            "Claro del Bosque": [antique_scroll]
        }

    def setup_sacred_objects(self):
        """
        Sets up the sacred objects required to complete the game.
        :return: A dictionary of sacred objects.
        """
        feather = Item(
            "Pluma Dorada", "Una pluma dorada brillante, parece tener un poder especial.")
        bell = Item("Campana de Plata",
                    "Una campana de plata antigua, con grabados místicos en su superficie.")

        self.sacred_objects_list.append(feather)
        self.sacred_objects_list.append(bell)

        return {
            "Enemigo Cueva": [feather],
            "Enemigo Lago": [bell]
        }

    def setup_sounds(self):
        # Get the directory where game.py is located
        base_path = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(base_path, os.pardir))  # Move up to the project root

        return os.path.join(project_root, 'audio')

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
                    fragment = Item(
                        "Fragmento de Cristal", "Un fragmento brillante que parece emitir una luz etérea.")
                    self.sacred_objects_list.append(fragment)
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
        spirit_dialogue = Dialogue([
            "El Espíritu Malévolo dice: 'Para obtener el fragmento de cristal, debes resolver tres acertijos...'",
            "'El primero lo encuentras aquí, en la Cueva Oscura, donde la luz no llega...'",
            "'El segundo está en el Lago Negro, donde las aguas profundas ocultan secretos olvidados..'",
            "'El tercero está en el Altar de Piedra, donde la luna brilla...'"
        ])

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
            "Cueva Oscura": spirit_dialogue,
            "Árbol de los Susurros": tree_dialogue,
            "Puente Roto": guardian_dialogue
        }

    def setup_enemies(self):
        """
        Configura los enemigos en diferentes ubicaciones del juego.
        :return: Un diccionario de enemigos mapeados a sus nombres de habitación correspondientes.
        """
        cave_enemy = Enemy("Guardia de las Sombras", "Un guardián de la oscuridad, vestido con una capa hecha de sombras.",
                   health=50, attack_power=15, inventory=self.sacred_objects["Enemigo Cueva"])
        lake_enemy = Enemy("Serpiente del Lago", "Una serpiente gigante que emerge del lago oscuro.",
                           health=80, attack_power=20, inventory=self.sacred_objects["Enemigo Lago"])

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
            if self.current_room.name == 'Puente Roto':
                self.finish_game()
        else:
            print("No hay nadie con quien hablar aquí.")

    
    # def play_sound_for_current_room(self, position="center"):
    #     room_key = self.current_room.name.lower().replace(" ", "_")
    #     if room_key in SOUNDS:
    #         song = SOUNDS[room_key]
    #         self.sound = Sound(os.path.join(self.audio_path, song), position)
    #         self.sound.play()

    # def play_sound_for_current_action(self, action, position="center", loop=False):
    #     if action in SOUNDS:
    #         song = SOUNDS[action]
    #         if action == 'hablar':
    #             song = song[self.current_room.name]
    #         self.sound = Sound(os.path.join(self.audio_path, song), position, loop)
    #         self.sound.play()
        
    def play_sound(self, room_name, action=False, position="center", loop=False):
        key = action if action else room_name.lower().replace(" ", "_")
        if key in SOUNDS:
            song = SOUNDS[key]
            if key == 'hablar': song = song[room_name]
            self.sound = Sound(os.path.join(self.audio_path, song), position, loop)
            self.sound.play()

    def use_item(self, item):
        if 0 < item and item <= len(self.player.inventory):
            object = self.player.inventory[item-1]
            object.use()
            if object.name == "Lampara de Aceite":
                self.show_enemies()
            if object.name == "Pergamino Antiguo":
                self.player.health = 100
        else:
            print("Seleccione un objeto de su inventario")

    def show_enemies(self):
        try:
            enemy = self.enemies[self.current_room.name]
            if enemy.is_alive():
                enemy.describe()
                sleep(1)
                enemy.attack(self.player)
                self.play_sound(self.current_room.name, enemy.name)
                self.fight_enemy(enemy)
            else:
                print("Ya has derrotado a los enemigos de esta habitacion!")
        except KeyError:
            print("No hay enemigos aqui!")

    def fight_enemy(self, enemy):
        while enemy.is_alive() and self.player.is_alive():
            print(f"\nTu salud: {self.player.health} | Salud de {enemy.name}: {enemy.health}")
            action = input(
                "¿Qué deseas hacer? ('atacar', 'defender', 'huir'):> ").strip().lower()

            if action == 'atacar':
                crtical_hit = random.random()
                if crtical_hit > 0.5:
                    print("¡Golpe crítico! ¡Haces el triple de daño!")
                    enemy.take_damage(30)
                    self.play_sound(self.current_room.name, action)
                else:
                    print(f"Atacas a {enemy.name} y le causas 10 de daño.\n")
                    self.play_sound(self.current_room.name, action)
                    enemy.take_damage(10)
                sleep(1.5)

                if enemy.is_alive():
                    print(f"{enemy.name} contraataca!\n")
                    sleep(1)
                    self.play_sound(self.current_room.name, enemy.name)
                    enemy.attack(self.player)

            elif action == 'defender':
                print("Te preparas para defenderte del próximo ataque.\n")
                sleep(1)
                self.play_sound(self.current_room.name, action)
                damage_taken = max(0, enemy.attack_power - 5)
                print(f"{enemy.name} te ataca, pero reduces el daño a {damage_taken}!")
                self.player.take_damage(damage_taken)

            elif action == 'huir':
                escape_chance = random.random()
                if escape_chance > 0.5:
                    print("Logras escapar del combate y esconderte\n")
                    self.play_sound(self.current_room.name, action)
                    sleep(3)
                    self.sound.stop()
                    self.current_room.describe()
                    return
                else:
                    print(
                        "Intentas huir, pero el enemigo te bloquea el camino y te ataca!")
                    sleep(1)
                    self.play_sound(self.current_room.name, enemy.name)
                    enemy.attack(self.player)

            else:
                print(
                    "Acción no válida. Por favor, elige 'atacar', 'defender' o 'huir'.")

            if not self.player.is_alive():
                print("Has sido derrotado... ¡Juego terminado!")
                self.play_sound(self.current_room.name, "explorador_derrotado")
                sleep(2)
                exit(1)

            if not enemy.is_alive():
                self.play_sound(self.current_room.name, "enemigo_derrotado")
                print(f"¡Has derrotado a {enemy.name}!")
                items = enemy.inventory
                self.sacred_objects_list.append(items)
                self.player.add_to_inventory(items)
                self.objective(items)
                self.current_room.describe()

    def objective(self, items):
        self.sacred_objects_collected += 1
        print(f"Has encontrado un {', '.join(item.name for item in items)}. Objetos sagrados recolectados: {self.sacred_objects_collected}/3.")
        if self.sacred_objects_collected == 3:
            print(
                "¡Has recolectado los tres objetos sagrados! Regresa al puente roto para escapar.")

    def move_player(self, direction):
        """
        Moves the player in a specified direction.
        :param direction: The direction the player wants to move.
        """
        self.current_room.mark_as_visited()
        next_room = self.current_room.get_room_in_direction(direction)

        if not next_room:
            print("No puedes ir en esa dirección.")
            return

        try:
            enemy = self.enemies[self.current_room.name]
            if enemy.is_alive() and not next_room.visited:
                print("No puedes ir en esa dirección. Aún hay cosas por explorar")
                return
        except KeyError:
            pass

        if self.current_room.name == 'Lago Negro' and direction != 'oeste':
            print(f'Decides navegar hacia el {direction}')
            self.play_sound("navegar")
            sleep(3)
            self.sound.stop()

        print("Decides seguir el sendero, tus pasos crujen sobre las hojas secas...")
        self.play_sound("caminar")

        sleep(3)
        self.sound.stop()
        self.current_room = next_room
        self.current_room.describe()
        self.play_sound(self.current_room.name, loop=True)
        if self.current_room.scene != "...":
            sleep(2)
            self.sound.stop()
            self.current_room.play_scene()
            self.play_sound(self.current_room.character)
        
    
    def finish_game(self):
        self.sound.stop()
        print("¿Qué deseas hacer?")
        print("1) Salir del bosque\n2) Regresar al bosque\n")
        action = int(input("> "))
        if action == 1:
            if self.sacred_objects_collected == 3:
                self.play_sound(self.current_room, "ganar")
                print("¡Has escapado del bosque encantado! ¡Felicidades!")
                sleep(2)
                exit(1)
            else:
                print("Debes recolectar los objetos sagrados antes de salir.")
        elif action == 2:
            if self.sacred_objects_collected == 3:
                for item in self.sacred_objects_list:
                    self.player.remove_from_inventory(item)
                print("Los objetos sagrados han sido eliminados de tu inventario. Quedas atrapado en el bosque para siempre.")
                print("¡Juego terminado!")
                sleep(2)
                exit(1)

    def collect_object(self, command):
        """
        Collects a sacred object in the current room, if available.
        """
        if self.current_room.name not in self.sacred_objects and self.current_room.name not in self.objects:
            print("No hay objetos que recolectar aquí.")
        else:
            if self.current_room.name in self.objects and self.current_room.items:
                items = self.objects[self.current_room.name]
                self.player.add_to_inventory(items)
                self.current_room.remove_item(items)
                self.play_sound(self.current_room.name, command)
                print(f"Has encontrado un {', '.join(item.name for item in items)}.")
            else:
                print("No hay objetos que recolectar aquí")

    def cleanup(self):
        self.sound.cleanup()

    def handle_commands(self, command):
        command.lower()
        if command in ["norte", "sur", "este", "oeste"]:
            self.sound.stop()
            self.move_player(command)
        elif command == "ver":
            self.current_room.look_around()
            self.play_sound(self.current_room.name, command)
        elif command == "hablar":
            self.play_sound(self.current_room.name, command, loop=True)
            self.play_dialogue()
            self.sound.stop()
        elif command.startswith("usar "):
            item = int(command.split(" ")[1])
            self.use_item(item)
        elif command == "inventario":
            self.player.show_inventory()
        elif command == "recoger":
            self.collect_object(command)
        elif command == "resolver":
            self.solve_puzzle()
        elif command == "salir":
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            exit(1)
        else:
            print("No entiendo ese comando.")

    def play(self):
        print("Bienvenido al bosque encantado!")
        self.play_sound(self.current_room.name, loop=True)
        self.current_room.describe()
        self.current_room.play_scene()
        self.current_room.mark_as_visited()
        try:
            while self.player.is_alive():
                command = input("> ").strip().lower()
                self.sound.stop()
                self.handle_commands(command)
        finally:
            self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.play()
