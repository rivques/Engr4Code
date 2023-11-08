import time
import adafruit_mpu6050
import busio
import board
import digitalio
import storage

sda_pin = board.GP14
scl_pin = board.GP15    
i2c = busio.I2C(scl_pin, sda_pin)

mpu = adafruit_mpu6050.MPU6050(i2c)

tilt_led = digitalio.DigitalInOut(board.GP16)
tilt_led.direction = digitalio.Direction.OUTPUT

status_led = digitalio.DigitalInOut(board.LED)
status_led.direction = digitalio.Direction.OUTPUT

while True: 
    accel = mpu.acceleration
    print(f"X: {accel[0]}m/s² Y: {accel[1]}m/s² Z: {accel[2]}m/s²")
    # are we not flat?
    # this is kinda naive and inflexible but it works for this case
    if abs(accel[2]) < 2:
        tilt_led.value = True
    else:
        tilt_led.value = False
    
    # log data
    if not storage.getmount("/").readonly:
        # we can write to the filesystem
        with open("/data.csv", "a") as datalog:
            written_string = f"{time.monotonic()},{accel[0]},{accel[1]},{accel[2]},{tilt_led.value}\n"
            datalog.write(written_string)
            datalog.flush()
            # blink onboard LED to indicate activity
            status_led.value = True
            time.sleep(0.1)
            status_led.value = False
            time.sleep(0.1)
    else:
        # sleep anyways
        time.sleep(0.2)