import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

broker = "iot.kmitlnext.com"
port = 9001

def on_message(client, userdata, message):
    print(f"Message received: {message.payload.decode()} + \n")
    if (message.payload.decode() == 0):
        client.publish("TanakornHome/LampSta" , "0")
        GPIO.output(4, False)
    else:
        client.publish("TanakornHome/LampSta" , "1")
        GPIO.output(4, True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Error, Connection failed")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

client = mqtt.Client(transprot="websockets")
client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.subscribe("TanakornHome/LampCmd")
client.loop_forever()
# except KeyboardInterrupt:
if KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    print("Exit")