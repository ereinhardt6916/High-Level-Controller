import I2C_LCD_driver
import logging
import RPi.GPIO as GPIO
from encoder import Encoder
from piece_locator import Piece_locator
from xy_selector import XY_selector
from shelper import Shelper
from gameManager import GameManager

# logging configuration
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

# variables for LCD
lcd = I2C_LCD_driver.lcd()

# variables for rotary encoder
GPIO.setmode(GPIO.BCM)
encoder_left = 27 #these are GPIO#, not pin#
encoder_right = 22
encoder_btn = 17
encoder = Encoder(encoder_left, encoder_right, encoder_btn)

# variables for piece locator
port_PL = "/dev/ttyACM0"
pl = Piece_locator(port_PL)

# variables for xy selector
port_XY = "/dev/ttyACM1"
xy = XY_selector(port_XY)

# variables for socket communication
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10236       # The port used by the server
socket = Shelper(HOST, PORT)

# variables for game init
gm = GameManager()