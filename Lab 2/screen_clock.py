import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fontForTimeOfWeek = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 23)
fontForTimeExact = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)


font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    image = Image.open("red.jpg")
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height /2
        scaled_height = height/2
    else:
        scaled_width = width/2
        scaled_height = image.height * width // image.width /2
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))


    clocktime = strftime("%H:%M:%S")
    dayWeek = strftime("%A")
    dateTime = strftime("%m/%d/%Y")
    y = top

    x_1 = width/2 - font.getsize(clocktime)[0]/2
    y_1 = height/2 - font.getsize(clocktime)[1]/2
    x_2 = width/2 - font.getsize(dayWeek)[0]/2
    y_2 = height/2 - font.getsize(dayWeek)[1] - font.getsize(clocktime)[1]/2

    x_3 = width/2 - font.getsize(dateTime)[0]/2
    y_3 = height/2 - font.getsize(dateTime)[1]/2
    # print("\r", end="", flush=True)

    if buttonA.value and not buttonB.value:
        # disp.fill(red)
        draw.text((x_3, y_3), dateTime, font=fontForTimeOfWeek, fill="#FFFFFF")
        # disp.image(image, rotation)


    else: 
        draw.text((x_1, y_1), clocktime, font=fontForTimeExact, fill="#FFFFFF")
        y += font.getsize(clocktime)[1]
        draw.text((x_2, y_2), dayWeek, font=fontForTimeOfWeek, fill="#FFFFFF")




    # y += font.getsize(IP)[1]
    # draw.text((x, y), WTTR, font=font, fill="#FFFF00")
    # y += font.getsize(WTTR)[1]
    # draw.text((x, y), USD, font=font, fill="#0000FF")
    # y += font.getsize(USD)[1]
    # draw.text((x, y), Temp, font=font, fill="#FF00FF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)