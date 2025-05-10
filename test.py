import serial
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load tones (040.wav to 049.wav)
tone_files = [f"{i:03}.wav" for i in range(40, 50)]
tones = [pygame.mixer.Sound(f) for f in tone_files]

# Connect to Arduino (adjust port as needed)
ser = serial.Serial('/dev/tty.usbmodem101', 115200)
print("Listening for analog activations...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("A") and line[1:].isdigit():
            pin_index = int(line[1:])
            if 0 <= pin_index < len(tones):
                print(f"Sensor A{pin_index} triggered")
                tones[pin_index].play()
            else:
                print(f"Out-of-range pin index: {pin_index}")
    except Exception as e:
        print(f"Error: {e}")
