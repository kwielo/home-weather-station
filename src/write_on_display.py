import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

display = Adafruit_SSD1306.SSD1306_128_64(rst=None)

display.begin()  # initialize graphics library for selected display module


def write(message, fsize=16):
    display.clear()  # clear display buffer
    display.display()  # write display buffer to physical display

    displayWidth = display.width  # get width of display
    displayHeight = display.height  # get height of display
    image = Image.new('1', (displayWidth, displayHeight))  # create graphics library image buffer
    draw = ImageDraw.Draw(image)  # create drawing object
    #font = ImageFont.load_default()  # load and set default font
    font = ImageFont.truetype("dogicapixel.ttf", size=fsize)

    draw.text((0,0), message, font=font, fill=255, spacing=4)

    display.image(image)  # set display buffer with image buffer
    display.display()  # write display buffer to physical display

    GPIO.cleanup()  # release all GPIO resources


def clear():
    display.clear()
    display.display()
    GPIO.cleanup()


clear()
