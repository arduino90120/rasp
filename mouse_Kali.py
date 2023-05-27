import RPi.GPIO as GPIO
import spidev
import ST7735
from PIL import Image, ImageDraw

# Set the GPIO mode and pin numbers
GPIO.setmode(GPIO.BCM)
X_PIN = 17
Y_PIN = 18

# Set SPI parameters
SPI_PORT = 0
SPI_DEVICE = 0

# Set LCD parameters
LCD_WIDTH = 128
LCD_HEIGHT = 128

# Initialize the SPI and LCD objects
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
lcd = ST7735.ST7735(dc=9, rst=25, spi=spi, width=LCD_WIDTH, height=LCD_HEIGHT)

# Initialize the analog mouse coordinates
x = 0
y = 0

# Define the callback function for X-axis
def x_callback(channel):
    global x
    x = GPIO.input(X_PIN)

# Define the callback function for Y-axis
def y_callback(channel):
    global y
    y = GPIO.input(Y_PIN)

# Setup interrupt pins
GPIO.setup(X_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(X_PIN, GPIO.BOTH, callback=x_callback)
GPIO.add_event_detect(Y_PIN, GPIO.BOTH, callback=y_callback)

try:
    while True:
        # Create a new image with a white background
        image = Image.new("RGB", (LCD_WIDTH, LCD_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Display the mouse coordinates
        draw.text((10, 10), f"X: {x}", fill=(0, 0, 0))
        draw.text((10, 30), f"Y: {y}", fill=(0, 0, 0))

        # Update the LCD display
        lcd.display(image)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Clean up GPIO settings
    GPIO.remove_event_detect(X_PIN)
    GPIO.remove_event_detect(Y_PIN)
    GPIO.cleanup()
    spi.close()
