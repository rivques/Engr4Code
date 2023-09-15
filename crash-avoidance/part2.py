import time
import adafruit_mpu6050
import busio
import board
import digitalio

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c)

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

while True:
    accel = mpu.acceleration
    print(f"X: {accel[0]}m/s² Y: {accel[1]}m/s² Z: {accel[2]}m/s²")
    time.sleep(0.5)
    # are we not flat?
    # this is kinda naive and inflexible but it works for this case
    if abs(accel[2]) < 1:
        led.value = True
    else:
        led.value = False