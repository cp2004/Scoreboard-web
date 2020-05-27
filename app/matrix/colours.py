from rgbmatrix import graphics

class Colours():
    def __init__(self):
        """Defining colours for matrix."""
        self.white = graphics.Color(255, 255, 255)
        self.blue = graphics.Color(0,0,150)
        self.green = graphics.Color(0,255,0)
        self.yellow = graphics.Color(255, 255, 0)
        self.red = graphics.Color(255,0,0)
        self.blank = graphics.Color(0,0,0)