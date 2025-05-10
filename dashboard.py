import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# CONFIGURATION
SERIAL_PORT = '/dev/tty.usbmodem101'  # Adjust as needed
BAUD_RATE = 115200
NUM_RFID = 7
NUM_PIEZO = 10

# --- State tracking ---
rfid_uid_valid = [False] * NUM_RFID
rfid_mapped_index = [-1] * NUM_RFID
piezo_states = ["Idle"] * NUM_PIEZO
solenoid_triggered = False

# --- Setup serial ---
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Connected to Arduino")

# --- Setup visualization ---
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Arduino Component Dashboard")

# Bar graphs
piezo_bar = ax1.bar(range(NUM_PIEZO), [0]*NUM_PIEZO)
ax1.set_title("Piezo Sensors (Activated = 1)")
ax1.set_ylim(0, 1)

rfid_bar = ax2.bar(range(NUM_RFID), [0]*NUM_RFID)
ax2.set_title("RFID UID Valid (1 = Valid)")
ax2.set_ylim(0, 1)

# --- Parsing function ---
def parse_line(line):
    global solenoid_triggered
    line = line.strip()

    if line.startswith("PIEZO_") and ",ACTIVATED" in line:
        index = int(line.split("_")[1].split(",")[0])
        piezo_states[index] = "Activated"

    elif line.startswith("READER_") and ",UID_VALID:" in line:
        parts = line.split(",")
        reader_id = int(parts[0].split("_")[1])
        uid_valid = parts[1].split(":")[1] == '1'
        mapped_index = int(parts[2].split(":")[1])

        rfid_uid_valid[reader_id] = uid_valid
        rfid_mapped_index[reader_id] = mapped_index

    elif line.startswith("SOLENOID_TRIGGER"):
        solenoid_triggered = True

    elif line.startswith("A"):
        # Handle additional info from A0–A6 triggers if needed
        pass

# --- Visualization updater ---
def update(frame):
    # Read any new serial lines
    while ser.in_waiting:
        line = ser.readline().decode('utf-8', errors='ignore')
        parse_line(line)

    # Update piezo bars
    for i, bar in enumerate(piezo_bar):
        bar.set_height(1 if piezo_states[i] == "Activated" else 0)

    # Update RFID bars
    for i, bar in enumerate(rfid_bar):
        bar.set_height(1 if rfid_uid_valid[i] else 0)

    # Reset piezo states for momentary visualization
    for i in range(NUM_PIEZO):
        if piezo_states[i] == "Activated":
            piezo_states[i] = "Idle"

    return piezo_bar + rfid_bar

ani = animation.FuncAnimation(fig, update, interval=200)
plt.tight_layout()
plt.show()
