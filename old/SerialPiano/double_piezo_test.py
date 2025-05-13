import serial
import time
import matplotlib.pyplot as plt
import numpy as np

# Set up serial communication (adjust port as needed)
ser = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)  # Change port if necessary
time.sleep(2)  # Allow time for the connection to establish

NUM_TRIALS = 10  # Number of trials
data = {"Piezo 0": [], "Piezo 1": []}  # Store readings for each trial
trial_data = []

def collect_trial():
    """Collect data for a single trial."""
    print("Starting trial... Drop the ball!")
    trial_piezo0 = []
    trial_piezo1 = []
    start_time = time.time()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            print(line)

            if "First" in line:
                value = int(line.split(": ")[1])
                trial_piezo0.append((time.time() - start_time, value))

            elif "Second" in line:
                value = int(line.split(": ")[1])
                trial_piezo1.append((time.time() - start_time, value))

        if time.time() - start_time > 5:  # Collect data for 5 seconds max
            break

    return trial_piezo0, trial_piezo1

# Run 10 trials
for trial in range(NUM_TRIALS):
    input(f"Press Enter to start Trial {trial + 1}...")  # Wait for user input
    piezo0_data, piezo1_data = collect_trial()
    trial_data.append((piezo0_data, piezo1_data))

# Close serial connection
ser.close()

# Plot the results
for i, (piezo0, piezo1) in enumerate(trial_data):
    plt.figure(figsize=(10, 5))

    if piezo0:
        times0, values0 = zip(*piezo0)
        plt.plot(times0, values0, label="Piezo 0", color="blue")

    if piezo1:
        times1, values1 = zip(*piezo1)
        plt.plot(times1, values1, label="Piezo 1", color="red")

    plt.xlabel("Time (s)")
    plt.ylabel("Piezo Sensor Reading")
    plt.title(f"Trial {i + 1} - Ball Drop Data")
    plt.legend()
    plt.grid()
    plt.show()

# Statistical Analysis
print("\n=== Statistical Analysis ===")
for i, (piezo0, piezo1) in enumerate(trial_data):
    p0_vals = [v for _, v in piezo0]
    p1_vals = [v for _, v in piezo1]

    print(f"\nTrial {i + 1}:")
    
    if p0_vals:
        print(f"  Piezo 0 - Max: {max(p0_vals)}, Mean: {np.mean(p0_vals):.2f}, Duration: {piezo0[-1][0]:.2f} sec")
    else:
        print("  Piezo 0 - No valid data.")

    if p1_vals:
        print(f"  Piezo 1 - Max: {max(p1_vals)}, Mean: {np.mean(p1_vals):.2f}, Duration: {piezo1[-1][0]:.2f} sec")
    else:
        print("  Piezo 1 - No valid data.")
