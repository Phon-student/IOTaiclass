import spidev
import time
import threading
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

# ---Thread Functions---#
def lab_1_r2():
    resistances = [10000, 5000, 20000]  # R2 = 10k, 10k//10k, 10k+10k
    ch = 0
    while True:
        for r2 in resistances:
            adc_value = read_spi(ch)
            voltage = calculate_voltage(adc_value)
            current = calculate_current(voltage, r2)
            calculated_r2 = voltage / current if current != 0 else float('inf')
            print(f"[Lab 1] R2: {r2} ohm | Voltage: {voltage:.2f} V | Current: {current:.2e} A | Measured R2: {calculated_r2:.2f} ohm")
            time.sleep(2)

def lab_2_ldr():
    ch_ldr = 1
    while True:
        adc_value = read_spi(ch_ldr)
        voltage = calculate_voltage(adc_value)
        if voltage > 1.5:  # Example threshold for light
            GPIO.output(GREEN_LED, GPIO.LOW)  # LED off
            print(f"[Lab 2] Room is bright (Voltage: {voltage:.2f} V). LED off.")
        else:
            GPIO.output(GREEN_LED, GPIO.HIGH)  # LED on
            print(f"[Lab 2] Room is dark (Voltage: {voltage:.2f} V). LED on.")
        time.sleep(2)

def lab_3_potentiometer():
    ch_pot = 2
    while True:
        adc_value = read_spi(ch_pot)
        voltage = calculate_voltage(adc_value)
        duty_cycle = (adc_value / 1023) * 100  # Scale to 0-100%
        pwm.ChangeDutyCycle(duty_cycle)
        print(f"[Lab 3] Potentiometer Voltage: {voltage:.2f} V | Duty Cycle: {duty_cycle:.2f}%")
        time.sleep(1)

# ---Main Function---#
if __name__ == '__main__':
    try:
        # Create threads for each lab
        thread_lab1 = threading.Thread(target=lab_1_r2, daemon=True)
        thread_lab2 = threading.Thread(target=lab_2_ldr, daemon=True)
        thread_lab3 = threading.Thread(target=lab_3_potentiometer, daemon=True)

        # Start threads
        thread_lab1.start()
        thread_lab2.start()
        thread_lab3.start()

        # Keep the main program running
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        spi.close()
        pwm.stop()
        GPIO.cleanup()
        print("\nSPI closed and GPIO cleaned up. Exiting...")
