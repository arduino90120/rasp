import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BCM)

btn_up = 5
btn_down = 26
btn_left = 19
btn_right = 6
btn_key1 = 21                  
btn_key2 = 20

# Up, Down, left, right, Button
GPIO.setup(btn_up, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(btn_down, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(btn_left, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(btn_right, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(btn_key1, GPIO.IN,GPIO.PUD_UP) #left button
GPIO.setup(btn_key2, GPIO.IN,GPIO.PUD_UP) #right button

    def main():
    m = PyMouse()
    KEY1_flag = False
    KEY2_flag = False
    KEY3_flag = False
    while True:  
        nowxy = m.position() 
        if (not GPIO.input(btn_key1)) and (not KEY1_flag ) : # button pressed 
            KEY1_flag = True
            print("KEY1")
            m.click(nowxy[0], nowxy[1], 1)
            
        if GPIO.input(btn_key1): # button released
            KEY1_flag = False
            
        if (not GPIO.input(btn_key2)and (not KEY2_flag )): # button pressed
            KEY2_flag = True
            print("KEY2")
            m.click(nowxy[0], nowxy[1], 2)
            
        if  GPIO.input(btn_key2): # button released
            KEY2_flag = False

        if (not GPIO.input(btn_up)): # button pressed
            m.move(nowxy[0] - 5, nowxy[1]) 

        if (not GPIO.input(btn_down)): # button pressed
            m.move(nowxy[0] + 5, nowxy[1]) 

        if (not GPIO.input(btn_left)): # button pressed
            m.move(nowxy[0], nowxy[1] + 5) 

        if (not GPIO.input(btn_right)): # button pressed
            m.move(nowxy[0], nowxy[1] - 5)
        
        time.sleep(0.02) # Poll every 20ms (otherwise CPU load gets too high)
        
if __name__ == "__main__":
    main()