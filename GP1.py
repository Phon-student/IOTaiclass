import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Pin Definitions
red = 17
yellow = 27
blue = 22
button = 18

# Setup pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial state
state = 0

# Function to set LED colors
def set_led(state):
    if state == 0:
        GPIO.output(red, 0)
        GPIO.output(yellow, 0)
        GPIO.output(blue, 0)
    elif state == 1:
        GPIO.output(red, 1)
        GPIO.output(yellow, 0)
        GPIO.output(blue, 0)
    elif state == 2:
        GPIO.output(red, 0)
        GPIO.output(yellow, 1)
        GPIO.output(blue, 0)
    elif state == 3:
        GPIO.output(red, 0)
        GPIO.output(yellow, 0)
        GPIO.output(blue, 1)
    elif state == 4:
        GPIO.output(red, 1)
        GPIO.output(yellow, 1)
        GPIO.output(blue, 0)
    elif state == 5:
        GPIO.output(red, 1)
        GPIO.output(yellow, 0)
        GPIO.output(blue, 1)
    elif state == 6:
        GPIO.output(red, 0)
        GPIO.output(yellow, 1)
        GPIO.output(blue, 1)
    elif state == 7:
        GPIO.output(red, 1)
        GPIO.output(yellow, 1)
        GPIO.output(blue, 1)

try:
    while True:
        button_state = GPIO.input(button)
        print(f"Button state: {button_state}")
        if button_state == 0:  # Button pressed
            state = (state + 1) % 8  # Cycle through 8 states
            print(f"State changed to: {state}")  # Debug print
            set_led(state)
            time.sleep(0.3)  # Debounce delay
        else:
            time.sleep(0.1)  # Polling delay
except KeyboardInterrupt:
    GPIO.cleanup()
