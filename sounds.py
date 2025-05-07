import serial
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load tones (assumes 10 .wav files: 040.wav to 049.wav)
tone_files = [
    "040.wav", "041.wav", "042.wav", "043.wav", "044.wav",
    "045.wav", "046.wav", "047.wav", "048.wav", "049.wav"
]
tones = [pygame.mixer.Sound(f) for f in tone_files]

# Map UID (as hex string) to tone index
uid_to_tone_index = {
    "AB12CD34": 0,
    "DEADBEEF": 1,
    "12345678": 2,
    "A1B2C3D4": 3,
    # Add more mappings as needed...
}

# Connect to Arduino
ser = serial.Serial('/dev/tty.usbmodem101', 115200)  # <-- update as needed

print("Listening for RFID-based step activations...")
while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("STEP"):
            step_label, uid_hex = line.split(":")
            step_index = int(step_label[4:])

            print(f"Step {step_index} activated — UID {uid_hex}")

            tone_index = uid_to_tone_index.get(uid_hex.upper(), None)
            if tone_index is not None and 0 <= tone_index < len(tones):
                tones[tone_index].play()
            else:
                print(f"Unknown UID: {uid_hex} — no tone mapped")
    except Exception as e:
        print(f"Error: {e}")
