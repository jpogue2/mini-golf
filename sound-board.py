import serial
import pygame
import time
import os

# Define mapping from characters to .mp3 file paths
NOTE_SOUNDS = {
    'C': "sounds/C1.mp3",
    'D': "sounds/D.mp3",
    'E': "sounds/E.mp3",
    'F': "sounds/F.mp3",
    'B': "sounds/B.mp3",
    'c': "sounds/C2.mp3",
    'V': "sounds/victory.mp3",
    'X': "sounds/bad.mp3"
}

# Initialize pygame mixer
pygame.mixer.init()

# Set the serial port and baud rate (adjust as needed)
SERIAL_PORT = '/dev/tty.usbmodem101'  # or "COM3" on Windows
BAUD_RATE = 9600

def play_note(note_char):
    file_path = NOTE_SOUNDS.get(note_char)
    if file_path and os.path.exists(file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        print(f"Playing: {file_path}")
    else:
        print(f"No sound for note: {note_char}")

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT}...")
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Received: {line}")
                    if len(line) == 1:
                        play_note(line)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
