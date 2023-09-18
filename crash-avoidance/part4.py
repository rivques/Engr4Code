import time
import adafruit_mpu6050
import busio
import board
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import digitalio
import terminalio
import displayio
import adafruit_mpl3115a2

# init displays
displayio.release_displays()

# init i2c
sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

# init display part 2
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=board.GP21)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# init IMU
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68)

# init baro
baro = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x60)
start_alt = baro.altitude

# init LED
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

# create the display group
splash = displayio.Group()

# empty title for now, will fill in later
text_area = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=5, y=5)
splash.append(text_area)    

# send display group to screen
display.show(splash)

while True:
    # log accel
    accel = mpu.acceleration
    print(f"X: {accel[0]}m/s² Y: {accel[1]}m/s² Z: {accel[2]}m/s²")
    
    # read gyro and barometer
    gyro = mpu.gyro
    altitude = baro.altitude
    # how far have we gone since we started?
    rel_altitude= altitude - start_alt

    # show data on OLED
    text_area.text = f"X: {gyro[0]: .3f}rad/s\nY: {gyro[1]: .3f}rad/s\nZ: {gyro[2]: .3f}rad/s\n Rel Alt: {rel_altitude:.1f}m"

    # sleep to not go too fast
    time.sleep(0.25)

    # are we not flat?
    # this is kinda naive and inflexible but it works for this case
    if abs(accel[2]) < 1 and rel_altitude < 3:
        led.value = True
    else:
        led.value = False