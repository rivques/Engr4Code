import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

MORSE_CODE = { 'A':'.-', 'B':'-...',
    'C':'-.-.', 'D':'-..', 'E':'.',
    'F':'..-.', 'G':'--.', 'H':'....',
    'I':'..', 'J':'.---', 'K':'-.-',
    'L':'.-..', 'M':'--', 'N':'-.',
    'O':'---', 'P':'.--.', 'Q':'--.-',
    'R':'.-.', 'S':'...', 'T':'-',
    'U':'..-', 'V':'...-', 'W':'.--',
    'X':'-..-', 'Y':'-.--', 'Z':'--..',
    '1':'.----', '2':'..---', '3':'...--',
    '4':'....-', '5':'.....', '6':'-....',
    '7':'--...', '8':'---..', '9':'----.',
    '0':'-----', ', ':'--..--', '.':'.-.-.-',
    '?':'..--..', '/':'-..-.', '-':'-....-',
    '(':'-.--.', ')':'-.--.-'}
base_delay = 0.25
CHAR_DELAYS = {
    ".": [base_delay, base_delay],
    "-": [3*base_delay, base_delay],
    " ": [0, 3*base_delay],
    "/": [0, 7*base_delay]
}

while True:
    user_input = input("Enter the string to translate, or type '-q' to quit. ")
    user_input = user_input.upper()
    if user_input == "-Q":
        break
    morse_translation = ""
    translation_good = True
    for letter in user_input:
        if letter == " ":
            morse_translation += "/"
        else:
            try:
                morse_translation += MORSE_CODE[letter] + " "
            except KeyError:
                print(f"Unsupported character \"{letter}\" used. Please try again.")
                translation_good = False
                break
    if translation_good:
        print(morse_translation)
        for pulse in morse_translation:
            on_delay, off_delay = CHAR_DELAYS[pulse]
            if on_delay == 0:
                time.sleep(off_delay)
            else:
                led.value = True
                time.sleep(on_delay)
                led.value = False
                time.sleep(off_delay)
            
print("Thanks for using the Morse Code Translator. Goodbye!")