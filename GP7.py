import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# MQTT Configuration
BROKER = "iot.kmitlnext.com"
PORT = 9001
USERNAME = "kmitliot"
PASSWORD = "KMITL@iot1234"

# MQTT Topics
TOPIC_LAMP = "TanakornHome/LampCmd"
TOPIC_LAMP_STATUS = "TanakornHome/LampSta"
TOPIC_RED = "TanakornHome/RGB/Red"
TOPIC_GREEN = "TanakornHome/RGB/Green"
TOPIC_BLUE = "TanakornHome/RGB/Blue"
TOPIC_RED_BRIGHTNESS = "TanakornHome/RGB/RedBrightness"

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LAMP_PIN = 4
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

GPIO.setup(LAMP_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# PWM for Red LED Brightness
red_pwm = GPIO.PWM(RED_PIN, 1000)  # 1 kHz frequency
red_pwm.start(0)  # Start with 0% duty cycle

# Callback Functions
def on_connect(client, _userdata, _flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe([(TOPIC_LAMP, 0), (TOPIC_RED, 0), (TOPIC_GREEN, 0), (TOPIC_BLUE, 0), (TOPIC_RED_BRIGHTNESS, 0)])
    else:
        print("Error, Connection failed")

def on_message(client, _userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Message received: {topic} -> {payload}")

    if topic == TOPIC_LAMP:
        state = payload == "1"
        GPIO.output(LAMP_PIN, state)
        client.publish(TOPIC_LAMP_STATUS, "1" if state else "0")

    elif topic == TOPIC_RED:
        GPIO.output(RED_PIN, payload == "1")

    elif topic == TOPIC_GREEN:
        GPIO.output(GREEN_PIN, payload == "1")

    elif topic == TOPIC_BLUE:
        GPIO.output(BLUE_PIN, payload == "1")

    elif topic == TOPIC_RED_BRIGHTNESS:
        try:
            brightness = int(payload)
            brightness = max(0, min(100, brightness))  # Clamp value between 0-100
            red_pwm.ChangeDutyCycle(brightness)
            print(f"Red LED Brightness: {brightness}%")
        except ValueError:
            print("Invalid brightness value")

def on_disconnect(client, _userdata, rc):
    print("Disconnected from broker.")

# MQTT Client Setup
client = mqtt.Client(transport="websockets")
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT)

# Start Loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    print("Exit")
