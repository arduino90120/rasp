#!/bin/bash

# Set SPI parameters
spi-config -d /dev/spidev0.0 -g 1000000

# Define LCD dimensions
LCD_WIDTH=128
LCD_HEIGHT=128

# Initialize LCD
function lcd_init() {
    gpio -g mode 25 out
    gpio -g mode 24 out
    gpio -g mode 23 out
    gpio -g mode 18 out
    
    # Reset the LCD
    gpio -g write 25 1
    gpio -g write 24 0
    sleep 0.05
    gpio -g write 25 0
    sleep 0.05
    gpio -g write 25 1
    sleep 0.05
    
    # Set LCD parameters
    echo -ne "\x37\x00\x0F\x01\x02\x08\x0F\x00\x01\x00" > /dev/spidev0.0
    sleep 0.1
}

# Send data to LCD
function lcd_write_data() {
    gpio -g write 18 1
    gpio -g write 23 1
    echo -ne "$1" > /dev/spidev0.0
    gpio -g write 23 0
    gpio -g write 18 0
}

# Clear the LCD screen
function lcd_clear() {
    for ((i=0; i<$LCD_HEIGHT; i++)); do
        for ((j=0; j<$LCD_WIDTH; j++)); do
            lcd_write_data "\x00"
        done
    done
}

# Draw a pixel on the LCD
function lcd_draw_pixel() {
    local x=$1
    local y=$2
    local color=$3
    
    if [[ $x -lt 0 || $x -ge $LCD_WIDTH || $y -lt 0 || $y -ge $LCD_HEIGHT ]]; then
        return
    fi
    
    lcd_write_data "\x80$((y & 0x7F))"
    lcd_write_data "\x80$((x & 0x7F))"
    lcd_write_data "$color"
}

# Main program
lcd_init

while true; do
    read -r -s -N 3 mouse_input < /dev/input/event0

    mouse_event=$(printf "%02X" "$(echo "$mouse_input" | cut -b 10-11)")
    mouse_code=$(printf "%02X" "$(echo "$mouse_input" | cut -b 9)")

    if [[ $mouse_event == "02" ]]; then
        # Handle X-axis movement
        x=$(printf "%d" "$((0x${mouse_code}))")
        # Adjust the scaling and direction of the mouse input as needed
        # You may need to experiment with the scaling factor to achieve the desired cursor movement
        scaled_x=$((x / 10))
    elif [[ $mouse_event == "01" ]]; then
        # Handle Y-axis movement
        y=$(printf "%d" "$((0x${mouse_code}))")
        # Adjust the scaling and direction of the mouse input as needed
        # You may need to experiment with the scaling factor to achieve the desired cursor movement
        scaled_y=$((y / 10))
    fi

    # Display cursor position on LCD
    lcd_clear
    lcd_draw_pixel $((LCD_WIDTH / 2 + scaled_x / 16)) $((LCD_HEIGHT / 2 + scaled_y / 16)) "\xFF"
done
