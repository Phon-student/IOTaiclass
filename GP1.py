import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


red = 17
yellow = 27
blue = 22

button = 18

GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        i = GPIO.input(button)

        #change each time button is pressed
        # 0 = off, 1 = red, 2 = yellow, 3 = blue
        # 4 = red + yellow, 5 = red + blue, 6 = yellow + blue

        if i == 0:
            GPIO.output(red, 0)
            GPIO.output(yellow, 0)
            GPIO.output(blue, 0)
        elif i == 1:
            GPIO.output(red, 1)
            GPIO.output(yellow, 0)
            GPIO.output(blue, 0)
        elif i == 2:
            GPIO.output(red, 0)
            GPIO.output(yellow, 1)
            GPIO.output(blue, 0)
        elif i == 3:
            GPIO.output(red, 0)
            GPIO.output(yellow, 0)
            GPIO.output(blue, 1)
        elif i == 4:
            GPIO.output(red, 1)
            GPIO.output(yellow, 1)
            GPIO.output(blue, 0)
        elif i == 5:
            GPIO.output(red, 1)
            GPIO.output(yellow, 0)
            GPIO.output(blue, 1)
        elif i == 6:
            GPIO.output(red, 0)
            GPIO.output(yellow, 1)
            GPIO.output(blue, 1)
        time.sleep(0.1)
finally:
    GPIO.cleanup()            

