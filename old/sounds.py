import serial
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load note sounds
note_sounds = {
    'C': pygame.mixer.Sound("c4-note.wav"),
    'D': pygame.mixer.Sound("d4-note.wav"),
    'E': pygame.mixer.Sound("e4-note.wav"),
}

# Map each step A0-A9 to a note
step_to_note = {
    0: 'D',
    1: 'D',
    2: 'D',
    3: 'E',
    4: 'E',
    5: 'E',
    6: 'D',
    7: 'C',
    8: 'D',
    9: 'E',
}

# Connect to Arduino (adjust port name if needed)
ser = serial.Serial('/dev/tty.usbmodem101', 115200)
print("Listening for analog activations...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("A") and line[1:].isdigit():
            step_index = int(line[1:])
            note = step_to_note.get(step_index)
            if note and note in note_sounds:
                print(f"Sensor A{step_index} triggered — Playing note {note}")
                note_sounds[note].play()
            else:
                print(f"Unknown note or unmapped step: A{step_index}")
    except Exception as e:
        print(f"Error: {e}")
