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

while True:
    user_input = input("Enter the string to translate, or type '-q' to quit. ")
    user_input = user_input.upper()
    if user_input == "-Q": # uppercase because of the previous line
        break
    morse_translation = ""
    translation_good = True # flag to be set if we hit an unknown character
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
            
print("Thanks for using the Morse Code Translator. Goodbye!")