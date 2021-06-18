import I2C_LCD_driver
import RPi.GPIO as GPIO
from encoder import Encoder
from piece_locator import Piece_locator
import time

# variables for LCD
mylcd = I2C_LCD_driver.lcd()

# variables for rotary encoder
GPIO.setmode(GPIO.BCM)

# variables for piece locator
port_PL = "/dev/ttyACM0"
pl = Piece_locator(port_PL)

def valueChanged(value):
    print(f"New value: {value}")
    mylcd.lcd_display_string(f"New value: {value}", 1)

def buttonPushed(channel):
    print(f"button push: {channel}")
    mylcd.lcd_display_string(f"button push: {channel}", 2)
    time.sleep(1)
    mylcd.lcd_display_string(' '*16, 2)
    

def main():

    e1 = Encoder(27, 22, 17, valueChanged, buttonPushed)

    try:
        while True:
            pl.print_data()
            time.sleep(1)
    except Exception as e:
        print(str(e))

    GPIO.cleanup()


if __name__ == "__main__":
    main()