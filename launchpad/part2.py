import time
import board
import digitalio

red = digitalio.DigitalInOut(board.GP16)
green = digitalio.DigitalInOut(board.GP17)
red.direction = digitalio.Direction.OUTPUT
green.direction = digitalio.Direction.OUTPUT

for i in range(10, 0, -1): # countdown
    print(i)
    red.value = True
    time.sleep(.2)
    red.value = False
    time.sleep(.8)

green.value = True #launch
print("Liftoff!")

while True:
    pass # infinite loop to keep the light on; it autoresets otherwise