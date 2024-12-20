import RPi.GPIO as GPIO
import threading
import time

# Setup GPIO
GPIO.setwarnings(False)
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

# Global flag for thread control
running = True

def thread1():  # RGB LED changes every 1 second
    while running:
        for i in range(8):
            set_led(i)
            time.sleep(1)

def thread2():  # PWM green LED
    pwm = GPIO.PWM(green, 100)
    pwm.start(0)
    try:
        while running:
            for i in range(10, 101, 10):
                pwm.ChangeDutyCycle(i)
                time.sleep(2)
            for i in range(100, 9, -10):
                pwm.ChangeDutyCycle(i)
                time.sleep(2)
    finally:
        pwm.stop()

def event():  # Button press, toggle red2 LED
    GPIO.remove_event_detect(button)
    GPIO.add_event_detect(button, GPIO.RISING, callback=button_callback, bouncetime=200)

def set_led(state):
    GPIO.output(red, bool(state & 0b001))
    GPIO.output(yellow, bool(state & 0b010))
    GPIO.output(blue, bool(state & 0b100))

def button_callback(channel):
    # Toggle the red2 LED
    GPIO.output(red2, not GPIO.input(red2))
    print(f"Red2 LED toggled to {'ON' if GPIO.input(red2) else 'OFF'}")

if __name__ == '__main__':
    try:
        # Start threads
        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)
        t1.start()
        t2.start()

        # Set up button event
        event()

        # Main loop
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Stop threads gracefully
        running = False
        t1.join()
        t2.join()
        GPIO.cleanup()
        print("GPIO Cleaned up")
