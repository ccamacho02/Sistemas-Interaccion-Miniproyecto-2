import openal

listener = openal.oalGetListener()

class Sound:
    def __init__(self, file_path, position='center'):
        self.source = openal.oalOpen(file_path)
        self.set_position_by_label(position)

    def play(self):
        self.source.play()

    def stop(self):
        self.source.stop()
    
    def set_position(self, position):
        self.source.set_position(position)

    def set_position_by_label(self, position_label):
        positions = {
            'left': (-10.0, 0.0, 0.0),
            'right': (1.0, 0.0, 0.0),
            'center': (0.0, 0.0, 0.0)
        }
        self.source.set_gain(10.0)
        self.set_position(positions.get(position_label, (0.0, 0.0, 0.0)))

    #listener.set_position(positions.get(position_label, (0.0, 0.0, 0.0)))
    
    def cleanup(self):
        self.stop()
        openal.oalQuit()