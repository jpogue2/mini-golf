import serial  # Library to communicate with serial devices (e.g., Arduino)
import pygame  # Library for handling sound playback
import os  # Library for file and directory operations
import tkinter as tk  # Library for GUI creation from tkinter import messagebox
# To display error messages (used minimally)
import threading  # Library to run tasks in parallel (background threads)

# Initialize the pygame mixer for playing sounds
pygame.mixer.init()

# Define the folder where sound files (.wav) are stored
sound_folder = os.path.join(os.getcwd(), "sounds")

# Dictionary to store preloaded sound objects
sound_library = {}


# Function to preload all sound files into memory at startup
def preload_sounds():
    global sound_library  # Access the global dictionary
    for file in os.listdir(sound_folder):  # List all files in the sounds folder
        if file.endswith('.wav'):  # Only process .wav files
            signal = file.split('.')[0]  # Extract the filename without extension (e.g., "001" from "001.wav")
            file_path = os.path.join(sound_folder, file)  # Full path to the file
            try:
                sound_library[signal] = pygame.mixer.Sound(file_path)  # Load the sound and store it
            except Exception as e:
                print(f"Error loading {file}: {e}")  # Print an error if loading fails


# Function to play a preloaded sound based on the signal received
def play_sound(signal):
    if signal in sound_library:  # Check if the sound exists in the dictionary
        sound_library[signal].play()  # Play the sound
    else:
        print(f"Sound file not found for signal: {signal}")  # Print error if sound is missing


# Setup the serial port for communication with an external device (e.g., Arduino)
serial_port = '/dev/cu.usbmodem101'  # Adjust this for your actual device
baud_rate = 9600  # Speed of communication (must match the sender)
ser = serial.Serial(serial_port, baud_rate, timeout=1)  # Create the serial connection with a 1-second timeout

# Create the main GUI window using Tkinter
root = tk.Tk()
root.title("Sound Player")  # Title of the window


# Function to create buttons for each available sound file
def create_sound_buttons():
    wav_files = sorted(sound_library.keys(), key=int)  # Sort filenames numerically (e.g., "001" before "010")

    for i, signal in enumerate(wav_files):  # Iterate over all available sound signals
        button = tk.Button(root, text=f"Play {signal}", command=lambda s=signal: play_sound(s))  # Create a button
        button.grid(row=i // 8, column=i % 8, padx=5, pady=5)  # Arrange buttons in a grid with 8 per row


# Function to read from the serial port and play the corresponding sound
def listen_serial():
    if ser.in_waiting > 0:  # Check if there is data waiting in the serial buffer
        signal = ser.readline().decode('utf-8').strip()  # Read a line, decode it, and remove whitespace
        if signal in sound_library:  # If the signal is a valid preloaded sound
            print(f"Playing: {signal}")  # Print confirmation
            play_sound(signal)  # Play the sound
    root.after(10, listen_serial)  # Schedule this function to run again in 10ms (non-blocking approach)


# Preload all sounds before running the UI
preload_sounds()

# Create buttons for all detected sound files
create_sound_buttons()

# Start listening to the serial port in a separate thread (so the GUI remains responsive)
threading.Thread(target=listen_serial, daemon=True).start()

# Start the Tkinter event loop (keeps the GUI running)
root.mainloop()
