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
                name1 = "Tanakorn        "
                name2 = "Youngmeesuk     "
                data1 = bytes(name1, 'ascii')
                data2 = bytes(name2, 'ascii')

                print(" sector 8 & 9 ")

                name1 = MIFAREReader.MFRC522_Readdata(8)
                name2 = MIFAREReader.MFRC522_Readdata(9)

                name1 = "".join(map(chr, name1))
                name2 = "".join(map(chr, name2))

                print(name1 + name2+"\n")
                print("Write data to sector 8 & 9")

                MIFAREReader.MFRC522_Write(8, data1)
                MIFAREReader.MFRC522_Write(9, data2)

                print("Write data to sector 8 & 9 success")

                name1 = MIFAREReader.MFRC522_Readdata(8)
                name2 = MIFAREReader.MFRC522_Readdata(9)

                name1 = "".join(map(chr, name1))
                name2 = "".join(map(chr, name2))

                print(name1 + name2+"\n")

                MIFAREReader.MFRC522_StopCrypto1()

                continue_reading = False
            else:
                print("Authentication error")