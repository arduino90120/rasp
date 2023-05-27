from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import spidev
import time
import pyautogui

# Set SPI parameters
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# Define LCD dimensions
LCD_WIDTH = 128
LCD_HEIGHT = 128

# Initialize LCD
def lcd_init():
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

# Move mouse cursor
def move_mouse(x, y):
    current_x, current_y = pyautogui.position()
    new_x = current_x + x
    new_y = current_y + y
    pyautogui.moveTo(new_x, new_y)

# Main program
if __name__ == '__main__':
    try:
        # Initialize LCD
        lcd_init()
        
        # Find the event device for the joystick
        devices = [InputDevice(path) for path in evdev.list_devices()]
        joystick = None

        for device in devices:
            if "mouse" in device.name.lower():
                joystick = device
                break

        if joystick is None:
            print("Joystick device not found.")
            exit()
        
        while True:
            for event in joystick.read_loop():
                if event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_X:
                        # Handle X-axis movement
                        x = event.value
                        # Adjust the scaling and direction of the joystick input as needed
                        # You may need to experiment with the scaling factor to achieve the desired cursor movement
                        scaled_x = int((x - 512) / 10)
                        move_mouse(scaled_x, 0)
                    elif event.code == ecodes.ABS_Y:
                        # Handle Y-axis movement
                        y = event.value
                        # Adjust the scaling and direction of the joystick input as needed
                        # You may need to experiment with the scaling factor to achieve the desired cursor movement
                        scaled_y = int((y - 512) / 10)
                        move_mouse(0, scaled_y)
                        
                    # Display joystick position on LCD
                    lcd_clear()
                    lcd_draw_pixel(LCD_WIDTH // 2 + scaled_x // 16, LCD_HEIGHT // 2 + scaled_y // 16, 0xFF)
    
    except KeyboardInterrupt:
        print("\nExiting...")
        spi.close()
        GPIO.cleanup()
