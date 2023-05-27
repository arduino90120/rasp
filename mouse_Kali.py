import RPi.GPIO as GPIO
import spidev
from waveshare_epd import epd1in44b

# Set the BCM GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for interrupt
INT_PIN = 17

# Set SPI parameters
SPI_PORT = 0
SPI_DEVICE = 0
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
spi.max_speed_hz = 1000000

# Initialize the e-paper display
epd = epd1in44b.EPD()
epd.init()

# Define callback function for interrupt
def interrupt_callback(channel):
    # Read mouse coordinates
    x = spi.xfer2([0x90, 0x00])[1] & 0x0F
    y = spi.xfer2([0xD0, 0x00])[1] & 0x0F
    print("X: {}, Y: {}".format(x, y))

# Setup interrupt pin
GPIO.setup(INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(INT_PIN, GPIO.FALLING, callback=interrupt_callback, bouncetime=10)

try:
    print("Analog mouse is ready. Press Ctrl+C to exit.")
    while True:
        # Clear the display
        epd.Clear(0xFF)
        # Display the mouse coordinates
        epd.draw_string_at(x=10, y=10, string="X: {}".format(x), font=None, color=0)
        epd.draw_string_at(x=10, y=30, string="Y: {}".format(y), font=None, color=0)
        epd.display()

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Clean up GPIO settings
    GPIO.remove_event_detect(INT_PIN)
    GPIO.cleanup()
    spi.close()
    epd.Dev_exit()
