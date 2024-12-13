#change LED color that connect to rpi gpio everytimes button is pressed
# only one LED is connected
# LED color will change from red, green, blue, yellow, cyan, magenta, white

import RPi.GPIO as GPIO
import time

# set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# set up GPIO pin as input and output
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# set up PWM
pwmR = GPIO.PWM(23, 100)
pwmG = GPIO.PWM(24, 100)

# start PWM with 0% duty cycle
pwmR.start(0)
pwmG.start(0)

# set up color
def setColor(r, g):
    pwmR.ChangeDutyCycle(r)
    pwmG.ChangeDutyCycle(g)

#on click swap color
def swapColor(color):
    if color == 'red':
        setColor(100, 0)
        return 'green'
    elif color == 'green':
        setColor(0, 100)
        return 'blue'
    elif color == 'blue':
        setColor(100, 100)
        return 'yellow'
    elif color == 'yellow':
        setColor(0, 100)
        return 'cyan'
    elif color == 'cyan':
        setColor(100, 0)
        return 'magenta'
    elif color == 'magenta':
        setColor(100, 100)
        return 'white'
    elif color == 'white':
        setColor(0, 0)
        return 'red'

color = 'red'
while True:
    input_state = GPIO.input(18)
    if input_state == False:
        color = swapColor(color)
        time.sleep(0.2)
# stop PWM
pwmR.stop()

# clean up GPIO
GPIO.cleanup()

