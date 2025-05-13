import tkinter as tk
import serial
import time
import threading

# CONFIGURATION
SERIAL_PORT = '/dev/tty.usbmodem101'  # Adjust this for your system
BAUD_RATE = 9600
NUM_RFID = 6
NUM_PIEZO = 10

# State tracking
rfid_uid_valid = [False] * NUM_RFID
rfid_mapped_index = [-1] * NUM_RFID
rfid_versions = [None] * NUM_RFID
rfid_connected = [False] * NUM_RFID
piezo_states = ["Idle"] * NUM_PIEZO
solenoid_triggered = False

# Serial setup
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

# --- GUI Setup ---
root = tk.Tk()
root.title("🔍 Live Puzzle System Dashboard")

header = tk.Label(root, text="Puzzle Status Dashboard", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Piezo status
piezo_frame = tk.LabelFrame(root, text="📍 Piezo Sensors", padx=10, pady=5)
piezo_frame.pack(fill="x", padx=10, pady=5)
piezo_labels = []
for i in range(NUM_PIEZO):
    label = tk.Label(piezo_frame, text=f"Step A{i}: —", width=20, relief="ridge", bg="lightgray")
    label.grid(row=i//5, column=i%5, padx=5, pady=2)
    piezo_labels.append(label)

# RFID status
rfid_frame = tk.LabelFrame(root, text="🔐 RFID Readers", padx=10, pady=5)
rfid_frame.pack(fill="x", padx=10, pady=5)
rfid_labels = []
for i in range(NUM_RFID):
    label = tk.Label(rfid_frame, text=f"Reader {i}: ❌ Mapped: None", width=40, relief="ridge", bg="lightcoral")
    label.grid(row=i//4, column=i%4, padx=5, pady=2)
    rfid_labels.append(label)

# Solenoid status
solenoid_label = tk.Label(root, text="🎯 Puzzle Solved: ❌ NO", font=("Arial", 14), bg="white")
solenoid_label.pack(pady=10, fill="x")

# --- Serial Parsing ---
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

    elif line.startswith("READER_") and ",VERSION:" in line:
        parts = line.split(",")
        reader_id = int(parts[0].split("_")[1])
        version_hex = parts[1].split(":")[1].replace("0x", "").upper()
        status_str = parts[2].split(":")[1]
        rfid_versions[reader_id] = version_hex
        rfid_connected[reader_id] = (status_str == "CONNECTED")

    elif line.startswith("SOLENOID_TRIGGER"):
        solenoid_triggered = True

# --- GUI Updater ---
def update_gui():
    # Update piezo labels
    for i, label in enumerate(piezo_labels):
        state = piezo_states[i]
        if state == "Activated":
            label.config(text=f"Step A{i}: ✅", bg="lightgreen")
            piezo_states[i] = "Idle"
        else:
            label.config(text=f"Step A{i}: —", bg="lightgray")

    # Update RFID labels
    for i, label in enumerate(rfid_labels):
        valid = rfid_uid_valid[i]
        mapped = rfid_mapped_index[i]
        version = rfid_versions[i] if rfid_versions[i] else "--"
        connected = rfid_connected[i]

        status = "✅" if valid else "❌"
        color = "lightgreen" if valid else "lightcoral"
        symbol = "🟢" if connected else "⚫"
        mapped_text = str(mapped) if mapped != -1 else "None"

        label.config(
            text=f"Reader {i}: {status} Mapped: {mapped_text}  V:{version} {symbol}",
            bg=color
        )

    # Solenoid label
    solenoid_label.config(
        text=f"🎯 Puzzle Solved: {'✅ YES' if solenoid_triggered else '❌ NO'}",
        bg="lightgreen" if solenoid_triggered else "white"
    )

    root.after(200, update_gui)

# --- Serial Reader Thread ---
def read_serial():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore')
            parse_line(line)

# Start serial reading thread
threading.Thread(target=read_serial, daemon=True).start()

# Start GUI loop
update_gui()
root.mainloop()
