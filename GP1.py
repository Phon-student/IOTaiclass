import RPi.GPIO as GPIO
import time

# Pin definitions
red_pin = 17
green_pin = 27
blue_pin = 22
button_pin = 18

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial LED state
current_color = 0

def set_color(color):
    GPIO.output(red_pin, color == 0)
    GPIO.output(green_pin, color == 1)
    GPIO.output(blue_pin, color == 2)

def button_callback(channel):
    global current_color
    current_color = (current_color + 1) % 3
    set_color(current_color)

# Cleanup GPIO to avoid edge detection failure
GPIO.cleanup()

# Setup event detection on button pin
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    set_color(current_color)
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
