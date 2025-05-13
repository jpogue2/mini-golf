import serial
import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load different sounds for each piezo sensor
sounds = {
    "First piezo": pygame.mixer.Sound("sounds/038.wav"),  # Change to actual sound file
    "Second piezo": pygame.mixer.Sound("sounds/055.wav")  # Change to actual sound file
}

# Set up serial communication (adjust port and baud rate as needed)
ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Change to the correct port

# Debounce duration settings (adjustable)
debounce_time = 0.15  # Prevents any sound from playing too soon after another sound
same_sound_debounce_time = 2.0  # Prevents the same sound from playing again too quickly

last_play_time = 0  # Track the last time any sound played
last_piezo_play_time = {"First piezo": 0, "Second piezo": 0}  # Track last play time for each piezo

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode("utf-8").strip()
            current_time = time.time()  # Get the current timestamp

            if data.startswith("First piezo:"):
                piezo_type = "First piezo"
                piezo_value = int(data.split(":")[1].strip())  # Extract value

            elif data.startswith("Second piezo:"):
                piezo_type = "Second piezo"
                piezo_value = int(data.split(":")[1].strip())  # Extract value

            else:
                continue  # Ignore unrecognized data

            # Check if the piezo value is above the threshold and debounce rules apply
            if piezo_value > 200 and \
               (current_time - last_play_time >= debounce_time) and \
               (current_time - last_piezo_play_time[piezo_type] >= same_sound_debounce_time):
                
                print(f"{piezo_type} Vibration detected: {piezo_value}")
                sounds[piezo_type].play()  # Play the corresponding sound
                
                last_play_time = current_time  # Update global debounce timer
                last_piezo_play_time[piezo_type] = current_time  # Update per-sensor debounce timer

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
