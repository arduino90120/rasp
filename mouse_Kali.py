import RPi.GPIO as GPIO
import spidev
import time

# Set SPI parameters
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# Define LCD dimensions
LCD_WIDTH = 128
LCD_HEIGHT = 128

# Initialize LCD
def lcd_init():
    # Initialize SPI communication
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    
    # Reset the LCD
    GPIO.output(25, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(25, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(25, GPIO.HIGH)
    time.sleep(0.05)
    
    # Set LCD parameters
    spi.writebytes([0x37, 0x00, 0x0F, 0x01, 0x02, 0x08, 0x0F, 0x00, 0x01, 0x00])
    time.sleep(0.1)

# Send data to LCD
def lcd_write_data(data):
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(23, GPIO.HIGH)
    spi.writebytes([data])
    GPIO.output(23, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

# Clear the LCD screen
def lcd_clear():
    for i in range(LCD_HEIGHT):
        for j in range(LCD_WIDTH):
            lcd_write_data(0x00)
            
# Draw a pixel on the LCD
def lcd_draw_pixel(x, y, color):
    if x < 0 or x >= LCD_WIDTH or y < 0 or y >= LCD_HEIGHT:
        return
    
    lcd_write_data(0x80 | (y & 0x7F))
    lcd_write_data(0x80 | (x & 0x7F))
    lcd_write_data(color)

# Read analog mouse position
def read_mouse():
    # Mouse channel selection (X/Y axis)
    chn = 0  # X-axis channel
    
    # Read analog mouse input
    mouse_pos = spi.xfer2([0x06, 0x00])
    raw_value = ((mouse_pos[0] & 0x0F) << 8) | mouse_pos[1]
    
    # Convert raw value to a range between -64 and 64
    value = raw_value if raw_value < 0x0800 else raw_value - 0x1000
    
    return value

# Main program
if __name__ == '__main__':
    try:
        # Initialize LCD
        lcd_init()
        
        while True:
            # Clear the LCD screen
            lcd_clear()
            
            # Read mouse position
            x = read_mouse()
            
            # Display mouse position on LCD
            lcd_draw_pixel(LCD_WIDTH // 2 + x // 16, LCD_HEIGHT // 2, 0xFF)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()
