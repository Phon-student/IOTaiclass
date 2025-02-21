import RPi.GPIO as GPIO
import MFRC522
import signal
import time

print
continue_reading = True

GPIO.setwarnings(False)

# --------------------------------------------------------------
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read")
    continue_reading = False
    GPIO.cleanup()

# --------------------------------------------------------------
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data write")
print("Press Ctrl-C to stop")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card read UID: ", uid[0], ":", uid[1], ":", uid[2], ":", uid[3])

            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                data1 = MIFAREReader.MFRC522_Readdata(8)
                data2 = MIFAREReader.MFRC522_Readdata(9)
                name = "".join(map(chr, data1))
                fname = "".join(map(chr, data2))
                print(name + fname)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")

    time.sleep(1)
