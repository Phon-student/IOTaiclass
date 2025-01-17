import spidev
import RPi.GPIO as GPIO
import time

# ---setup SPI---#
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# ---read spi---#
def read_spi(channel):
    raw = spi.xfer2([1, (channel << 4) | 0x80, 0])
    data = ((raw[1] & 3) << 8) | raw[2]
    return data


if __name__ == "__main__":
    try:
        while True:
            adc_value = read_spi(0)
            voltage = (adc_value / 1024) * 3.3
            print(f"ADC Value: {adc_value} | Voltage: {voltage:.2f} V")
            time.sleep(1)
    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()
        print("\nBye!")