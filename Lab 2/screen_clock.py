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

pomodoroClockFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)


t = 25*60


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    clocktime = strftime("%H:%M:%S")
    dayWeek = strftime("%A")
    dateTime = strftime("%m/%d/%Y")


    y = top

    x_1 = width/2 - font.getsize(clocktime)[0]/2
    y_1 = height/2 - font.getsize(clocktime)[1]/2
    x_2 = width/2 - font.getsize(dayWeek)[0]/2
    y_2 = height/2 - font.getsize(dayWeek)[1] - font.getsize(clocktime)[1]/2

    x_3 = width/2 - font.getsize(dateTime)[0]/2 + 2
    y_3 = height/2 - font.getsize(dateTime)[1]/2


    if buttonB.value and not buttonA.value:

        draw.text((x_3, y_3), dateTime, font=fontForTimeOfWeek, fill="#FFFFFF")

        mins = t//60
        secs = t%60
        currentt = "{:02d}:{:02d}".format(mins, secs)

        timer = "Pomodoro Timer: "
        draw.text((x_3, y_3+26), timer, font=pomodoroClockFont, fill="#FFFFFF")
        draw.text((x_3, y_3+44), currentt, font=pomodoroClockFont, fill="#FFFFFF")
        t -=1
        # draw.text((x_3, y_3+20), 'Time to rest.', font=fontForTimeOfWeek, fill="#FFFFFF")



        draw.line([(x_3, y_3-10), (x_3+100, y_3-10)], fill="red", width=3)
        draw.line([(x_3, y_3-13), (x_3+95, y_3-13)], fill="orange", width=3)
        draw.line([(x_3, y_3-16), (x_3+90, y_3-16)], fill="yellow", width=3)
        draw.line([(x_3, y_3-19), (x_3+85, y_3-19)], fill="green", width=3)
        draw.line([(x_3, y_3-22), (x_3+80, y_3-22)], fill="blue", width=3)
        draw.line([(x_3, y_3-25), (x_3+75, y_3-25)], fill="purple", width=3)

        disp.image(image, rotation)


    else: 
        draw.text((x_1, y_1), clocktime, font=fontForTimeExact, fill="#FFFFFF")
        y += font.getsize(clocktime)[1]
        draw.text((x_2, y_2), dayWeek, font=fontForTimeOfWeek, fill="#FFFFFF")
        disp.image(image, rotation)


    # Display image.
    time.sleep(1)