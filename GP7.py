import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# MQTT Broker Information
broker = "iot.kmitlnext.com"
port = 9001

green_pin = 17
blue_pin = 27
red_pin = 22  # Red LED for on/off
red_pwm_pin = 18  # Red LED for dimming

def update_led_status():
    """Turn off all LEDs if none are active."""
    if GPIO.input(green_pin) or GPIO.input(blue_pin) or GPIO.input(red_pin):
        print("At least one LED is on")
    else:
        pwm_red.ChangeDutyCycle(0)
        GPIO.output(red_pin, False)
        print("All LEDs Off")

def on_message(client, _userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Message received: {topic} - {payload}")
    
    if topic == "TanakornHome/Green":
        GPIO.output(green_pin, payload == "1")
        print(f"Green {'On' if payload == '1' else 'Off'}")
    
    elif topic == "TanakornHome/Blue":
        GPIO.output(blue_pin, payload == "1")
        print(f"Blue {'On' if payload == '1' else 'Off'}")
    
    elif topic == "TanakornHome/Red":
        GPIO.output(red_pin, payload == "1")
        print(f"Red {'On' if payload == '1' else 'Off'}")
    
    elif topic == "TanakornHome/RedDim":
        try:
            dim_value = int(payload)  # Convert to integer
            if 0 <= dim_value <= 100:
                pwm_red.ChangeDutyCycle(dim_value)  # Adjust brightness
                print(f"LED Dim {dim_value}%")
        except ValueError:
            print("Invalid brightness value received.")
    
    update_led_status()

def on_connect(client, _userdata, _flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("TanakornHome/Green")
        client.subscribe("TanakornHome/Blue")
        client.subscribe("TanakornHome/Red")
        client.subscribe("TanakornHome/RedDim")
    else:
        print("Error, Connection failed")

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(red_pwm_pin, GPIO.OUT)
pwm_red = GPIO.PWM(red_pwm_pin, 1000)  # PWM frequency
pwm_red.start(0)  # Start with 0% duty cycle

# MQTT Setup
client = mqtt.Client(transport="websockets")
client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
try:
    client.loop_forever()
except KeyboardInterrupt:
    pwm_red.stop()
    GPIO.cleanup()
    client.disconnect()
    print("Exit")