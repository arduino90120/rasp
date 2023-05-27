#!/bin/bash

# Find the event device for the mouse
mouse_device=$(grep -E 'Handlers|EV' /proc/bus/input/devices | grep -B1 'EV=17' | grep -Eo 'event[0-9]+')

# Mouse movement scaling factor
scaling_factor=10

# Mouse cursor movement function
function move_cursor() {
    local x=$1
    local y=$2
    
    # Adjust the scaling and direction of the mouse input as needed
    # You may need to experiment with the scaling factor to achieve the desired cursor movement
    local scaled_x=$((x / scaling_factor))
    local scaled_y=$((y / scaling_factor))
    
    # Move the mouse cursor
    xdotool mousemove_relative --sync $scaled_x $scaled_y
}

# Main program
while true; do
    # Read the mouse input event
    read -r -s -N 3 mouse_input < "/dev/input/${mouse_device}"
    
    # Extract the mouse movement data
    mouse_event=$(printf "%02X" "$(echo "$mouse_input" | cut -b 10-11)")
    mouse_code=$(printf "%02X" "$(echo "$mouse_input" | cut -b 9)")

    if [[ $mouse_event == "02" ]]; then
        # Handle X-axis movement
        x=$(printf "%d" "$((0x${mouse_code}))")
        move_cursor $x 0
    elif [[ $mouse_event == "01" ]]; then
        # Handle Y-axis movement
        y=$(printf "%d" "$((0x${mouse_code}))")
        move_cursor 0 $y
    fi
done
