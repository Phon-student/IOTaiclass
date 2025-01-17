import spidev
import time
import RPi.GPIO as GPIO

# ---setup SPI---#
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# ---GPIO Setup---#
GPIO.setmode(GPIO.BCM)
GREEN_LED = 17  # Green LED for LDR
RED_LED = 18    # Red LED for potentiometer (PWM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

# Initialize PWM for Red LED
pwm = GPIO.PWM(RED_LED, 1000)  # 1 kHz frequency
pwm.start(0)

# ---read SPI---#
def read_spi(channel):
    raw = spi.xfer2([1, (channel << 4) | 0x80, 0])
    data = ((raw[1] & 3) << 8) | raw[2]
    return data

# ---Voltage and Current Calculation---#
def calculate_voltage(adc_value, v_ref=3.3, resolution=1024):
    return (adc_value / resolution) * v_ref

def calculate_current(voltage, resistance):
    return voltage / resistance if resistance != 0 else 0

# ---Loop Functions---#
def lab_1_r2():
    # Initial Resistance R2
    resistances = [10000, 5000, 20000]  # R2 = 10k, 10k//10k, 10k+10k
    ch = 0
    for r2 in resistances:
        adc_value = read_spi(ch)
        voltage = calculate_voltage(adc_value)
        current = calculate_current(voltage, r2)
        calculated_r2 = voltage / current if current != 0 else float('inf')
        print(f"R2 Setup: {r2} ohm | Voltage: {voltage:.2f} V | Current: {current:.2e} A | Measured R2: {calculated_r2:.2f} ohm")
        time.sleep(2)

def lab_2_ldr():
    ch_ldr = 1
    while True:
        adc_value = read_spi(ch_ldr)
        voltage = calculate_voltage(adc_value)
        if voltage > 1.5:  # Example threshold for light
            GPIO.output(GREEN_LED, GPIO.LOW)  # LED off
            print(f"Room is bright (Voltage: {voltage:.2f} V). LED off.")
        else:
            GPIO.output(GREEN_LED, GPIO.HIGH)  # LED on
            print(f"Room is dark (Voltage: {voltage:.2f} V). LED on.")
        time.sleep(2)

def lab_3_potentiometer():
    ch_pot = 2
    while True:
        adc_value = read_spi(ch_pot)
        voltage = calculate_voltage(adc_value)
        duty_cycle = (adc_value / 1023) * 100  # Scale to 0-100%
        pwm.ChangeDutyCycle(duty_cycle)
        print(f"Potentiometer Voltage: {voltage:.2f} V | Duty Cycle: {duty_cycle:.2f}%")
        time.sleep(1)

# ---Main Loop---#
if __name__ == '__main__':
    try:
        print("Running Lab 1: Measure R2")
        lab_1_r2()
        print("\nRunning Lab 2: LDR")
        lab_2_ldr()
        print("\nRunning Lab 3: Potentiometer")
        lab_3_potentiometer()
    except KeyboardInterrupt:
        spi.close()
        pwm.stop()
        GPIO.cleanup()
        print("\nSPI closed and GPIO cleaned up. Exiting...")
