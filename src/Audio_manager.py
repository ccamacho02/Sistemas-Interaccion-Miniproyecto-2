import openal
from math import cos, sin
from time import sleep

listener = openal.oalGetListener()

class Sound:
    def __init__(self, file_path, position='center', loop=False):
        self.source = openal.oalOpen(file_path)
        self.set_position_by_label(position)
        self.source.set_looping(loop)

    def play(self):
        self.source.play()

    def stop(self):
        self.source.stop()
    
    def set_position(self, position):
        self.source.set_position(position)

    def set_position_by_label(self, position_label):
        positions = {
            'left': (-50.0, 0.0, 0.0),
            'right': (1.0, 0.0, 0.0),
            'center': (0.0, 0.0, 0.0),
            'bottom': (0.0, 0.0, 10.0),
        }
        self.source.set_gain(10.0)
        self.set_position(positions.get(position_label, (0.0, 0.0, 0.0)))
    
    def set_movement(self):
        for angle in range(0, 360, 90):
            rad = angle * 3.14159 / 180.0
            listener.set_orientation((cos(rad), 0, -sin(rad), 0, 1, 0))
            self.play()
            sleep(3)
        

    #listener.set_position(positions.get(position_label, (0.0, 0.0, 0.0)))
    
    def cleanup(self):
        self.stop()
        openal.oalQuit()