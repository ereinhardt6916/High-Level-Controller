import time
import logging
import random
import RPi.GPIO as GPIO
from config import lcd, xy, pl, encoder, socket, gm


def valueChanged(value):
    logging.info(f"New value: {value}")
    lcd.lcd_display_string(f"New value: {value}", 1)

def buttonPushed(channel):
    logging.info(f"button push: {channel}")
    lcd.lcd_display_string(f"button push: {channel}", 2)
    time.sleep(1)
    lcd.lcd_display_string(' '*16, 2)
    

def main():
    try:
        logging.info("[main]Program started")

        # hardware init
        xy.selector_init()
        encoder.callbackAttach(valueChanged, buttonPushed)

        # game manager init
        gm.setup(socket, xy, pl, encoder, lcd)


        # start the game loop
        # gm.startGame()

        # while True:
        #     cmd = str(input("cmd: "))
        #     xy.directCmd(cmd)
        
    except Exception as e:
        logging.info(str(e))

    gm.startGame()

    GPIO.cleanup()


if __name__ == "__main__":
    main()