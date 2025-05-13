import serial
import time
import tkinter as tk

# Replace with your Arduino's serial port (e.g., "COM3" on Windows, "/dev/ttyUSB0" on Linux/Mac)
SERIAL_PORT = "/dev/cu.usbmodem101"
BAUD_RATE = 9600
CARD_TIMEOUT = 0.1  # Time in seconds before considering the card missing

class RFIDReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Card Status")
        
        # Display label
        self.status_label = tk.Label(root, text="Waiting for card...", font=("Arial", 32), fg="white", bg="black", width=20, height=5)
        self.status_label.pack(expand=True, fill="both")

        # Serial setup
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)  # No delay in serial reading
        except serial.SerialException:
            self.status_label.config(text="Serial Port Error", bg="red")
            return

        self.last_card_time = time.time()
        self.check_serial()

    def check_serial(self):
        """Continuously read from serial without delay"""
        try:
            while self.ser.in_waiting:  # Check if data is available
                line = self.ser.readline().decode('utf-8').strip()
                print(line)
                if line:
                    self.status_label.config(text="Card Present", bg="green")
                    self.last_card_time = time.time()

            # If no data received for a while, show "Card Missing"
            if time.time() - self.last_card_time > CARD_TIMEOUT:
                self.status_label.config(text="Card Missing", bg="red")

        except Exception:
            self.status_label.config(text="Error", bg="red")

        self.root.after(10, self.check_serial)  # Update every 10ms for near-instant response

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDReaderApp(root)
    root.mainloop()
