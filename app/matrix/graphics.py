import time
import os
import sys

from PIL import Image
sys.path.append('/home/pi/rpi-rgb-led-matrix/bindings/python')  # Should be configurable?
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


white = graphics.Color(255, 255, 255)
blue = graphics.Color(0, 0, 150)
green = graphics.Color(0, 255, 0)
yellow = graphics.Color(255, 255, 0)
red = graphics.Color(255, 0, 0)
blank = graphics.Color(0, 0, 0)

basedir = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(basedir, 'resources')

ScoreFont = graphics.Font()
ScoreFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '6x13.bdf'))

winFont = graphics.Font()
winFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '5x8.bdf'))

connectFont = graphics.Font()
connectFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '6x10.bdf'))

initialFont = graphics.Font()
initialFont.LoadFont(os.path.join(RESOURCES_DIR, 'fonts', '4x6.bdf'))


def InitMatrix():
    """Class for calling all graphical functions for the matrix."""
    # OPTIONS
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 0
    options.multiplexing = 0
    options.pwm_bits = 11
    options.brightness = 100
    options.pwm_lsb_nanoseconds = 130
    options.led_rgb_sequence = "RGB"
    options.pixel_mapper_config = ""
    options.gpio_slowdown = 3
    options.drop_privileges = 0
    options.daemon = 0
    # Test speed
    # options.show_refresh_rate = 1 #~530HZ on wiimote version

    return RGBMatrix(options=options)


def Scores(matrix, Player1Score, Player2Score, Serving, Player1Initial=None, Player2Initial=None):
    P1txt = "{:02}".format(int(Player1Score))
    P2txt = "{:02}".format(int(Player2Score))
    matrix.Clear()
    graphics.DrawText(matrix, ScoreFont, 1, 10, white, P1txt)  # canvas, font, xpos, ypos, color, text
    graphics.DrawLine(matrix, 13, 5, 18, 5, white)
    graphics.DrawText(matrix, ScoreFont, 20, 10, white, P2txt)

    graphics.DrawText(matrix, initialFont, 3, 16, red, Player1Initial)
    graphics.DrawText(matrix, initialFont, 22, 16, red, Player2Initial)

    if Serving == 1:
        graphics.DrawLine(matrix, 0, 10, 15, 10, yellow)
    else:
        graphics.DrawLine(matrix, 16, 10, 31, 10, yellow)


def Start(matrix):
    matrix.Clear()
    graphics.DrawText(matrix, ScoreFont, 1, 10, white, "Starting")


def Clear(matrix):
    matrix.Clear()


def WinAnimation(matrix, queue, name):
    # Animation celebrating the winner
    # Pulsing brightness
    max_brightness = matrix.brightness
    count = 0
    while count <= 6:
        if matrix.brightness < 1:
            matrix.brightness = max_brightness
            count += 1
        else:
            matrix.brightness -= 1

        if count % 2 == 0:
            matrix.Fill(255, 0, 0)
        elif count % 2 == 1:
            matrix.Fill(0, 255, 0)

        if not queue.empty():
            queue.get()
            matrix.Clear()
            return
        time.sleep(0.004)

    # Theaterchase with player text
    image1 = Image.open(os.path.join(RESOURCES_DIR, 'images', 'Win-Chase-1.png')).convert('RGB')
    image2 = Image.open(os.path.join(RESOURCES_DIR, 'images', 'Win-Chase-2.png')).convert('RGB')
    wintxt = '{} WINS'.format(name)
    count = 0
    xpos = 2
    colour = red
    direction = "left"
    while count <= 100:
        matrix.Clear()

        if count % 2 == 0:
            matrix.SetImage(image1, unsafe=False)
        elif count % 2 == 1:
            matrix.SetImage(image2, unsafe=False)

        if 25 <= count < 50 or 75 <= count:
            colour = green
        else:
            colour = red

        graphics.DrawText(matrix, connectFont, xpos, 11, colour, wintxt)

        if not queue.empty():
            queue.get()
            matrix.Clear()
            return
        time.sleep(0.1)

        count += 1
        if direction == "left":
            xpos -= 1
            if (len(wintxt) * 6) - 28 == -(xpos - 2):
                direction = "right"
        else:
            xpos += 1
            if -2 == -(xpos - 2):
                direction = "left"

    matrix.Clear()
