import time
import board
import digitalio

red = digitalio.DigitalInOut(board.GP16)
green = digitalio.DigitalInOut(board.GP17)
red.direction = digitalio.Direction.OUTPUT
green.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

def checkedSleep(length):
    SLEEPTIME = 0.05
    for i in range(length//SLEEPTIME):
        time.sleep(SLEEPTIME)
        if not button.value:
            return True
    return False

while button.value: # wait for button press
    pass

for i in range(10, 0, -1): # countdown
    print(i)
    red.value = True
    if i == 10: # give time to release the button
        time.sleep(.2)
    else:
        if checkedSleep(.2):
            print("ABORT!")
            break

    red.value = False
    if i == 10: # give time to release the button
        time.sleep(.8)
    else:
        if checkedSleep(.8): # give time to release the button
            print("ABORT!")
            break
else:
    green.value = True #launch
    print("Liftoff!")

while True:
    pass # infinite loop to keep the light on; it autoresets otherwise