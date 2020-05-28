#handle each screen with calls from the mainloop
#Also initialize and setup matrix
import time, os, sys
sys.path.append('/home/pi/rpi-rgb-led-matrix/bindings/python')
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image
from .colours import Colours

basedir = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(basedir, 'resources')

class Matrix():
    def __init__(self):
        """Class for calling all graphical functions for the matrix."""
        #OPTIONS
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        #self.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.gpio_slowdown = 2
        options.drop_privileges = 0
        options.daemon = 0
        # Test speed
        #options.show_refresh_rate = 1 #~530HZ on wiimote version
        print("Initialising matrix...")
        self.matrix = RGBMatrix(options = options)
        print("done")
        #FONTS
        self.ScoreFont = graphics.Font()
        self.ScoreFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '6x13.bdf')) #6px X 9px
        self.winFont = graphics.Font()
        self.winFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '5x8.bdf'))
        #COLOURS
        self.colour = Colours()

    def Scores(self, Player1Score, Player2Score, Serving):
        print("Showing scores!")
        P1txt = "{:02}".format(int(Player1Score))
        P2txt = "{:02}".format(int(Player2Score))
        self.matrix.Clear()
        graphics.DrawText(self.matrix, self.ScoreFont, 1, 10, self.colour.white, P1txt) # canvas, font, xpos, ypos, color, text
        graphics.DrawLine(self.matrix, 13, 5, 18, 5, self.colour.white)
        graphics.DrawText(self.matrix, self.ScoreFont, 20, 10, self.colour.white, P2txt)

        if Serving == 1:
            graphics.DrawLine(self.matrix, 0, 11, 15, 11, self.colour.yellow)
        else:
            graphics.DrawLine(self.matrix, 16, 11, 31, 11, self.colour.yellow)
    

    def WinAnimation(self, name):
        #Animation celebrating the winner
        #Pulsing brightness
        max_brightness = self.matrix.brightness
        count = 0
        while count <= 6:
            if self.matrix.brightness < 1:
                self.matrix.brightness = max_brightness
                count += 1
            else:
                self.matrix.brightness -= 1

            if count % 2 == 0:
                self.matrix.Fill(255,0,0)
            elif count % 2 == 1:
                self.matrix.Fill(0,255,0)
            time.sleep(0.004)
        
        #Theaterchase with player text
        image1 = Image.open(os.path.join(RESOURCES_DIR, 'images', 'Win-Chase-1.png')).convert('RGB')
        image2 = Image.open(os.path.join(RESOURCES_DIR, 'images', 'Win-Chase-2.png')).convert('RGB')
        wintxt = '{} WINS'.format(name)
        count = 0
        xpos = 2
        colour = self.colour.red
        direction = "left"
        while count <= 100:
            self.matrix.Clear()

            if count % 2 == 0:
                self.matrix.SetImage(image1)
            elif count % 2 == 1:
                self.matrix.SetImage(image2)
            
            if 25 <= count < 50 or 75 <= count:
                colour = self.colour.green
            else:
                colour = self.colour.red
            
            graphics.DrawText(self.matrix, self.connectFont, xpos, 11, colour, wintxt)
            time.sleep(0.1)
            count += 1
            if direction == "left":
                xpos -= 1
                if (len(wintxt)*6) - 28 == -(xpos - 2):
                    direction = "right"
            else:
                xpos += 1
                if -2 == -(xpos -2):
                    direction = "left"

    def SelectBox(self, Left, Right, Colour):
        graphics.DrawLine(self.matrix, Left, 0, Right, 0, Colour)
        graphics.DrawLine(self.matrix, Right, 0, Right, 10, Colour)
        graphics.DrawLine(self.matrix, Right, 10, Left, 10, Colour)
        graphics.DrawLine(self.matrix, Left, 10, Left, 0, Colour)