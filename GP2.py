import RPi.GPIO as GPIO
import _thread
import time

#two paralle threads and 1 events
#main task : RGBLE change every 1 second
#event task : button press, LED on/off
#sub thread : Green LED dim in cycle 10 -> 20-> 100 -> 10 -> 20 every 2 second 

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Pin Definitions
red = 17
yellow = 27
blue = 22
button = 18
green = 10
red2 = 9  

# Setup pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red2, GPIO.OUT)

def thread1(): #RGBLED change every 1 second
    while True:
        for i in range(8):
            set_led(i)
            time.sleep(1)

def thread2(): #PWM green LED
    #PWM
    pwm = GPIO.PWM(green, 100)
    pwm.start(0)
    while True:
        for i in range(10, 101, 10):
            pwm.ChangeDutyCycle(i)
            time.sleep(2)
        for i in range(100, 9, -10):
            pwm.ChangeDutyCycle(i)
            time.sleep(2)


def event(): #button press, LED on/off of red2 LED
    GPIO.add_event_detect(button, GPIO.RISING, callback=button_callback, bouncetime=200)

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

def button_callback(channel):
    #read the state of the button
    button_state = GPIO.input(button)
    print(f"Button state: {button_state}")

    #toggle the red2 LED
    if GPIO.input(red2):
        GPIO.output(red2, 0)
    else:
        GPIO.output(red2, 1)

        
if __name__ == '__main__':
    try:
        _thread.start_new_thread(thread1, ())
        _thread.start_new_thread(thread2, ())
        event()
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO Cleaned up")