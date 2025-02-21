import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import paho.mqtt.client as mqtt
import requests

continue_reading = True

def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read")
    continue_reading = False
    GPIO.cleanup()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    signal.signal(signal.SIGINT, end_read)

def read_card(MIFAREReader):
    status, TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print("Card detected")
        status, uid = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("Card read UID: ", uid[0], ":", uid[1], ":", uid[2], ":", uid[3])
            return uid
    return None

def authenticate_card(MIFAREReader, uid):
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    MIFAREReader.MFRC522_SelectTag(uid)
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
    if status == MIFAREReader.MI_OK:
        data1 = MIFAREReader.MFRC522_Readdata(8)
        data2 = MIFAREReader.MFRC522_Readdata(9)
        name = "".join(map(chr, data1)).strip()
        fname = "".join(map(chr, data2)).strip()
        MIFAREReader.MFRC522_StopCrypto1()
        return f"{name}_{fname}"
    else:
        print("Authentication error")
        return None

def send_data_to_server(name):
    data = {"tname": "tanakorn", "name": name}
    response = requests.post("http://iot.kmitlnext.com/iot/lab/insert.php", data=data)
    if response.text == '1':
        print("Record to DB successfully")
        client = mqtt.Client(transport="websockets")
        client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
        client.connect("iot.kmitlnext.com", 9001)
        client.publish("tanakorn/table", "1")
    else:
        print("Fail to record to DB")

def main():
    setup()
    MIFAREReader = MFRC522.MFRC522()
    print("Welcome to the MFRC522 data write")
    print("Press Ctrl-C to stop")

    while continue_reading:
        uid = read_card(MIFAREReader)
        if uid:
            name = authenticate_card(MIFAREReader, uid)
            if name:
                send_data_to_server(name)
        time.sleep(1)

if __name__ == "__main__":
    main()
