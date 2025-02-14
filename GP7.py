import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# MQTT Broker Information
broker = "iot.kmitlnext.com"
port = 9001

green_pin = 17
blue_pin = 27
red_pin = 22  # Red LED for on/off
red_pwm_pin = 18  # Red LED for dimming

def on_message(client, _userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Message received: {topic} - {payload}")

    if topic == "TanakornHome/Green":
        if payload == "1":
            GPIO.output(green_pin, True)
            print("Green On")
        else:
            GPIO.output(green_pin, False)
            print("Green Off")
    
    elif topic == "TanakornHome/Blue":
        if payload == "1":
            GPIO.output(blue_pin, True)
            print("Blue On")
        else:
            GPIO.output(blue_pin, False)
            print("Blue Off")
    
    elif topic == "TanakornHome/Red":
        if payload == "1":
            GPIO.output(red_pin, True)
            print("Red On")
        else:
            GPIO.output(red_pin, False)
            print("Red Off")
    
    elif topic == "TanakornHome/RedDim":
        try:
            dim_value = int(payload)  # Convert to integer
            if 0 <= dim_value <= 100:
                pwm_red.ChangeDutyCycle(dim_value)  # Adjust brightness
                print(f"LED Dim {dim_value}%")
        except ValueError:
            print("Invalid brightness value received.")

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
