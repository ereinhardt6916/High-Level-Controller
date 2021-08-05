import time
import logging
import random
import RPi.GPIO as GPIO
from config import lcd, xy, pl, encoder, socket, gm, watchdog


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

        # watchdog init
        watchdog.start(lcd)
        
        # game manager init
        gm.setup(socket, xy, pl, encoder, lcd)
        encoder.callbackAttach(valueChanged, buttonPushed)

        # start the game loop
        while True:
            try:
                gm.startGame()
            except Exception as e:
                logging.info(str(e))

        # demo_layout = [ \
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # demo_layout = [ \
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 2, 2, 2, 1, 1],\
        # [ 1, 1, 2, 2, 0, 2, 2, 1, 1]]

        # gm.startDemo(layout=demo_layout)
        
    except Exception as e:
        logging.info(str(e))

    GPIO.cleanup()



if __name__ == "__main__":
    main()