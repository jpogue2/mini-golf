import pygame
import numpy as np
import time
import random

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def generate_fairy_note(freq, duration=0.4, volume=0.5, wobble_depth=4, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Pitch wobble using sine LFO
    wobble = np.sin(2 * np.pi * 5 * t) * wobble_depth
    freq_variation = freq + wobble
    wave = np.sin(2 * np.pi * freq_variation * t)

    # Add gentle sparkle harmonic
    sparkle = 0.2 * np.sin(2 * np.pi * freq * 2.5 * t)

    # Combine base and sparkle
    signal = wave + sparkle

    # Normalize and pan
    signal = signal * (2**15 - 1) * volume
    signal = signal.astype(np.int16)

    # Stereo panning
    pan = random.uniform(0.2, 0.8)
    left = (signal * (1 - pan)).astype(np.int16)
    right = (signal * pan).astype(np.int16)
    stereo = np.column_stack((left, right))

    return pygame.sndarray.make_sound(stereo)

# Whimsical enchanted scale
fairy_notes = [659, 740, 784, 880, 988, 1047, 1175, 1319, 1175, 988]

# Play the magical melody
for freq in fairy_notes:
    tone = generate_fairy_note(freq)
    tone.play()
    time.sleep(0.4)
