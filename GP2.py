import RPi.GPIO as GPIO
import _thread
import time

# Two parallel threads and 1 event:
# Main task: RGB LED changes every 1 second.
# Event task: Button press, toggles a red2 LED on/off.
# Sub-thread: Green LED dims in cycles (10 -> 20 -> 100 -> 10 -> 20 every 2 seconds).

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

# LED color states
color_states = {
    0: (0, 0, 0),  # All off
    1: (1, 0, 0),  # Red
    2: (0, 1, 0),  # Yellow
    3: (0, 0, 1),  # Blue
    4: (1, 1, 0),  # Orange (Red + Yellow)
    5: (1, 0, 1),  # Purple (Red + Blue)
    6: (0, 1, 1),  # Cyan (Yellow + Blue)
    7: (1, 1, 1),  # White (Red + Yellow + Blue)
}

# Thread 1: RGB LED changes every second
def thread1():
    while True:
        for state in color_states:
            set_led(state)
            time.sleep(1)

# Thread 2: PWM Green LED dimming
def thread2():
    pwm = GPIO.PWM(green, 100)
    pwm.start(0)
    while True:
        for duty_cycle in range(10, 101, 10):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(2)
        for duty_cycle in range(100, 9, -10):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(2)

# Event: Button press toggles red2 LED on/off
def event():
    GPIO.add_event_detect(button, GPIO.RISING, callback=button_callback, bouncetime=200)

# Set LED colors based on state
def set_led(state):
    if state in color_states:
        GPIO.output(red, color_states[state][0])
        GPIO.output(yellow, color_states[state][1])
        GPIO.output(blue, color_states[state][2])
    else:
        print(f"Invalid LED state: {state}")

# Button callback: Toggle red2 LED
def button_callback(channel):
    current_state = GPIO.input(red2)
    GPIO.output(red2, not current_state)
    print(f"Red2 LED toggled to {'ON' if not current_state else 'OFF'}")

# Main program
if __name__ == '__main__':
    try:
        # Start threads using _thread
        _thread.start_new_thread(thread1, ())
        _thread.start_new_thread(thread2, ())
        # Start event detection
        event()
        # Keep the main thread running
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO cleaned up")
