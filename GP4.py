import spidev
import time


# ---setup SPI---#
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# ---read---#
def read_spi(channel):
    raw = spi.xfer2([1, (channel<<4)|0x80, 0])
    data = ((raw[1]&3) << 8) | raw[2]
    return data

# ---loop---#

if __name__ == '__main__':
    ch = 0
    try:
        while True:
            val = read_spi(ch)
            print(f"ADC Value: {val}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        spi.close()
        print("SPI closed")
        exit(0)