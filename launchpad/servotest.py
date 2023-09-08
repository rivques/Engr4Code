import board
import pwmio
import adafruit_motor.servo

pwm = pwmio.PWMOut(board.GP15, duty_cycle=2**15, frequency=50)
servo = adafruit_motor.servo.Servo(pwm, min_pulse=750, max_pulse=2250)
servo.angle = 0

while True:
    servo.angle = int(input("input angle: "))