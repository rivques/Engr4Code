import time
import board
import digitalio
import pwmio
import adafruit_motor.servo

pwm = pwmio.PWMOut(board.GP15, duty_cycle=2 ** 15, frequency=50)
servo = adafruit_motor.servo.Servo(pwm, min_pulse=500, max_pulse=2500)
servo.angle = 0

red = digitalio.DigitalInOut(board.GP16)
green = digitalio.DigitalInOut(board.GP17)
red.direction = digitalio.Direction.OUTPUT
green.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

def interpolate(x, in_min, in_max, out_min, out_max):
    # from Arduino map()
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def checked_servo_wait(servo, button, i, startTime, waitTime):
    # sweep the servo AND check if the abort gets pressed
    endTime = startTime + waitTime
    while time.monotonic() < endTime:
        if not button.value:
            print("ABORT!")
            servo.angle = 0
            return False
        if i < 4:
            time_left = 1-(time.monotonic()-startTime)+i
            # print(f"{time_left} left")
            servo.angle = interpolate(time_left, 4, 1, 0, 180)
    return True


while button.value:  # wait for button press
    pass


for i in range(10, 0, -1):  # countdown
    print(i)
    red.value = True
    startTime = time.monotonic()
    if i == 10:  # give time to release the button
        time.sleep(.2)
    else:
        if not checked_servo_wait(servo, button, i, startTime, .2):
            break

    red.value = False
    if i == 10:  # give time to release the button
        time.sleep(.8)
    else:
        if not checked_servo_wait(servo, button, i, startTime, .8):
            break
else:
    green.value = True  # launch
    print("Liftoff!")

while True:
    pass  # infinite loop to keep the light on; it autoresets otherwise
