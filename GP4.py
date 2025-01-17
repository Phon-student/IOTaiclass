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

# ---Voltage Calculation---#
def calculate_voltage(adc_value, v_ref=3.3, resolution=1024):
    return (adc_value / resolution) * v_ref


# ---Thread Functions---#
def lab_1_r2():
    ch = 0
    while True:
        adc_value = read_spi(ch)
        voltage = calculate_voltage(adc_value)
        resistance = (voltage * 1000) / (3.3 - voltage)  # R2 = (Vout * R1) / (Vin - Vout)
        current = voltage / resistance
        print(f"[Lab 1] Voltage: {voltage:.2f} V | Resistance: {resistance:.2f} Ohm | Current: {current} mA")
        time.sleep(2)
    

def lab_2_ldr():
    ch_ldr = 1
    while True:
        adc_value = read_spi(ch_ldr)
        voltage = calculate_voltage(adc_value)
        if voltage > 2:
            GPIO.output(GREEN_LED, 1)
            print(f"[Lab 2] LDR Voltage: {voltage:.2f} V | Green LED ON")
        else:
            GPIO.output(GREEN_LED, 0)
            print(f"[Lab 2] LDR Voltage: {voltage:.2f} V | Green LED OFF")
        time.sleep(2)

def lab_3_potentiometer():
    ch_pot = 2
    while True:
        adc_value = read_spi(ch_pot)
        voltage = calculate_voltage(adc_value)
        duty_cycle = (adc_value / 1023) * 100  # Scale to 0-100%
        pwm.ChangeDutyCycle(duty_cycle)
        print(f"[Lab 3] Potentiometer Voltage: {voltage:.2f} V | Duty Cycle: {duty_cycle:.2f}%")
        time.sleep(2)

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
