import I2C_LCD_driver
import RPi.GPIO as GPIO
from encoder import Encoder
from piece_locator import Piece_locator
from xy_selector import XY_selector
import time
import logging

# variables for LCD
mylcd = I2C_LCD_driver.lcd()

# variables for rotary encoder
GPIO.setmode(GPIO.BCM)

# variables for piece locator
port_PL = "/dev/ttyACM0"
pl = Piece_locator(port_PL)

# variables for xy selector
port_XY = "/dev/ttyACM1"
xy = XY_selector(port_XY)

def valueChanged(value):
    logging.info(f"New value: {value}")
    mylcd.lcd_display_string(f"New value: {value}", 1)

def buttonPushed(channel):
    logging.info(f"button push: {channel}")
    mylcd.lcd_display_string(f"button push: {channel}", 2)
    time.sleep(1)
    mylcd.lcd_display_string(' '*16, 2)
    

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("[main]Program started")

    e1 = Encoder(27, 22, 17, valueChanged, buttonPushed)

    try:
        # test xy control
        xy.executeCmd(["home", ['x', 1], ['y', 5], ['s', 1, 5], "z0"])
        while True:
            if pl.isNewPiece():
                logging.info("[main]new piece: " + str(pl.getNewCoordinate()))

            time.sleep(0.1)
    except Exception as e:
        logging.info(str(e))

    GPIO.cleanup()


if __name__ == "__main__":
    main()