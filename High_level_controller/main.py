import time
import logging
import random
import RPi.GPIO as GPIO
from config import lcd, xy, pl, encoder, socket, gm


def valueChanged(value):
    # logging.info(f"New value: {value}")
    # lcd.lcd_display_string(f"New value: {value}", 1)
    gm.encoderTriggered(value)

def buttonPushed(channel):
    # logging.info(f"button push: {channel}")
    # lcd.lcd_display_string(f"button push: {channel}", 2)
    # time.sleep(1)
    # lcd.lcd_display_string(' '*16, 2)
    gm.buttonPushed()
    

def main():
    try:
        logging.info("[main]Program started")

        # hardware init
        xy.selector_init()
        
        # game manager init
        gm.setup(socket, xy, pl, encoder, lcd)
        encoder.callbackAttach(valueChanged, buttonPushed)

        # start the game loop
        while True:
            try:
                gm.startGame()
            except Exception as e:
                logging.info(str(e))
        
    except Exception as e:
        logging.info(str(e))

    GPIO.cleanup()


if __name__ == "__main__":
    main()