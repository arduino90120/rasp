import evdev

# Open mouse device
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
mouse = None
for device in devices:
    if "mouse" in device.name.lower():
        mouse = evdev.InputDevice(device.path)
        break

if mouse is None:
    print("Mouse not found. Please make sure it is connected.")
    exit()

# Open joystick device
joystick = None
for device in devices:
    if "joystick" in device.name.lower():
        joystick = evdev.InputDevice(device.path)
        break

if joystick is None:
    print("Joystick not found. Please make sure it is connected.")
    exit()

# Main loop
for event in mouse.read_loop():
    if event.type == evdev.ecodes.EV_REL:
        if event.code == evdev.ecodes.REL_X:
            # Handle X-axis movement
            x_pos = event.value
            print("Mouse X-axis:", x_pos)

        elif event.code == evdev.ecodes.REL_Y:
            # Handle Y-axis movement
            y_pos = event.value
            print("Mouse Y-axis:", y_pos)

    elif event.type == evdev.ecodes.EV_KEY:
        if event.code == evdev.ecodes.BTN_LEFT:
            # Handle left button press/release
            if event.value == 1:
                # Left button pressed
                print("Left button pressed")
            elif event.value == 0:
                # Left button released
                print("Left button released")

        elif event.code == evdev.ecodes.BTN_RIGHT:
            # Handle right button press/release
            if event.value == 1:
                # Right button pressed
                print("Right button pressed")
            elif event.value == 0:
                # Right button released
                print("Right button released")

# Main loop for joystick
for event in joystick.read_loop():
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == evdev.ecodes.ABS_X:
            # Handle X-axis movement
            x_pos = event.value
            print("Joystick X-axis:", x_pos)

        elif event.code == evdev.ecodes.ABS_Y:
            # Handle Y-axis movement
            y_pos = event.value
            print("Joystick Y-axis:", y_pos)

    elif event.type == evdev.ecodes.EV_KEY:
        if event.code == evdev.ecodes.BTN_TRIGGER:
            # Handle button press/release
            if event.value == 1:
                # Button pressed
                print("Button pressed")
            elif event.value == 0:
                # Button released
                print("Button released")
