import RPi.GPIO as GPIO
import time

GPIO.cleanup()
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
    if color == 0:
        GPIO.output(red_pin, GPIO.HIGH)
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(blue_pin, GPIO.LOW)
    elif color == 1:
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.HIGH)
        GPIO.output(blue_pin, GPIO.LOW)
    elif color == 2:
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(blue_pin, GPIO.HIGH)

def button_callback(channel):
    global current_color
    current_color = (current_color + 1) % 3
    set_color(current_color)
    
# Setup event detection on button pin
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()