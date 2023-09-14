import time
import adafruit_mpu6050
import busio
import board

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    accel = mpu.acceleration
    print(f"X: {accel[0]}m/s² Y: {accel[1]}m/s² Z: {accel[2]}m/s²")
    time.sleep(0.5)