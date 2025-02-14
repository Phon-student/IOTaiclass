import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

broker = "iot.kmitlnext.com"
port = 9001

def on_message(client, _userdata, message):
    print(f"Message received: {message.payload.decode()} + \n")
    if (message.payload.decode() == "0"):
        client.publish("TanakornHome/LampSta" , "0")
        GPIO.output(17, False)
    else:
        client.publish("TanakornHome/LampSta" , "1")
        GPIO.output(17, True)

def on_connect(_client, _userdata, _flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Error, Connection failed")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

client = mqtt.Client(transport="websockets")
client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.subscribe("TanakornHome/LampCmd")
try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    print("Exit")