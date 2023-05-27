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

# Read analog joystick position
def read_joystick():
    # Joystick channel selection (X/Y axis)
    x_chn = 0  # X-axis channel
    y_chn = 1  # Y-axis channel
    
    # Read analog joystick input
    x_pos = spi.xfer2([0x06 | (x_chn >> 2), (x_chn & 0x03) << 6, 0x00])
    y_pos = spi.xfer2([0x06 | (y_chn >> 2), (y_chn & 0x03) << 6, 0x00])
    
    x_raw_value = ((x_pos[1] & 0x0F) << 8) | x_pos[2]
    y_raw_value = ((y_pos[1] & 0x0F) << 8) | y_pos[2]
    
    # Convert raw values to a range between -64 and 64
    x_value = x_raw_value if x_raw_value < 0x0800 else x_raw_value - 0x1000
    y_value = y_raw_value if y_raw_value < 0x0800 else y_raw_value - 0x1000
    
    return x_value, y_value

# Read button status
def read_buttons():
    # Button channel selection
    btn_chn = 2  # Button channel
    
    # Read button status
    button = spi.xfer2([0x06 | (btn_chn >> 2), (btn_chn & 0x03) << 6, 0x00])
    
    # Check button status (0 = pressed, 1 = released)
    return 0 if (button[1] & 0x04) == 0 else 1

# Main program
if __name__ == '__main__':
    try:
        # Initialize LCD
        lcd_init()
        
        while True:
            # Clear the LCD screen
            lcd_clear()
            
            # Read joystick position
            x, y = read_joystick()
            
            # Display joystick position on LCD
            lcd_draw_pixel(LCD_WIDTH // 2 + x // 16, LCD_HEIGHT // 2 + y // 16, 0xFF)
            
            # Read button status
            button_status = read_buttons()
            
            # Display button status on LCD
            if button_status == 0:
                lcd_draw_pixel(LCD_WIDTH // 2, LCD_HEIGHT - 1, 0xFF)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()
