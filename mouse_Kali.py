import RPi.GPIO as GPIO
import spidev
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from waveshare_epd import epd1in44

# Set the GPIO mode and pin numbers
GPIO.setmode(GPIO.BCM)
JOY_X = 17
JOY_Y = 18
JOY_BTN = 27

# Set SPI parameters
SPI_PORT = 0
SPI_DEVICE = 0

# Initialize the SPI and LCD objects
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
epd = epd1in44.EPD()
epd.init()

# Set up the image and font
image = Image.new("1", (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

# Initialize the joystick coordinates and button state
joy_x = 0
joy_y = 0
joy_btn = True

# Define the callback function for joystick X-axis
def x_callback(channel):
    global joy_x
    joy_x = GPIO.input(JOY_X)

# Define the callback function for joystick Y-axis
def y_callback(channel):
    global joy_y
    joy_y = GPIO.input(JOY_Y)

# Define the callback function for joystick button
def btn_callback(channel):
    global joy_btn
    joy_btn = not GPIO.input(JOY_BTN)

# Setup interrupt pins
GPIO.setup(JOY_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOY_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(JOY_X, GPIO.BOTH, callback=x_callback)
GPIO.add_event_detect(JOY_Y, GPIO.BOTH, callback=y_callback)
GPIO.add_event_detect(JOY_BTN, GPIO.BOTH, callback=btn_callback)

try:
    while True:
        # Clear the image
        draw.rectangle((0, 0, epd.width, epd.height), fill=255)

        # Draw joystick position and button state
        draw.text((10, 10), f"X: {joy_x}", font=font, fill=0)
        draw.text((10, 30), f"Y: {joy_y}", font=font, fill=0)
        draw.text((10, 50), f"Button: {'Pressed' if joy_btn else 'Released'}", font=font, fill=0)

        # Display the image
        epd.display(epd.getbuffer(image))

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Clean up GPIO settings
    GPIO.remove_event_detect(JOY_X)
    GPIO.remove_event_detect(JOY_Y)
    GPIO.remove_event_detect(JOY_BTN)
    GPIO.cleanup()
    spi.close()
    epd.Dev_exit()
