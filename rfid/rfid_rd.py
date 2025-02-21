import RPi.GPIO as GPIO
import MFRC522
import signal
import time


continue_reading = True


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

MIFAREReader = MFRC522.MFRC522()

print("Welcome to the MFRC522 data write ")
print("Press Ctrl-C to stop.")

while continue_reading:

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected")

    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:

        print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))

        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        MIFAREReader.MFRC522_SelectTag(uid)

        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        if status == MIFAREReader.MI_OK:
            data1 = MIFAREReader.MFRC522_Read_Readdata(8)
            data2 = MIFAREReader.MFRC522_Read_Readdata(9)
            name =  "".join(map(chr, data1)) 
            fname =  "".join(map(chr, data2))
            print(name + fname)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")

        time.sleep(1)
