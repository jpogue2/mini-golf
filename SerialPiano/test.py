import serial
import pygame

# Initialize pygame mixer
pygame.mixer.init()
sound = pygame.mixer.Sound("sounds/038.wav")  # Replace with the path to your sound file

# Set up serial communication (adjust port and baud rate as needed)
ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Change "COM3" to your Arduino's port

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode("utf-8").strip()
            if data.isdigit() and int(data) > 0:  # Check if the piezo sensor detected a vibration
                print(f"Vibration detected: {data}")
                sound.play()
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
