import tkinter as tk
from threading import Thread
from Arduino_related_code.ArduinoDigital import ArduinoDigital
from Arduino_related_code.ValveControl import ValveControl
import time

def calibrate_valve(pin, duration_ms, arduino):
    valve_control = ValveControl(pin, arduino)
    duration_s = duration_ms / 1000  # Convert duration from milliseconds to seconds

    for i in range(25):
        print(f"Calibrating valve on pin {pin}: Iteration {i+1}")
        valve_control.OpenValve(duration_s)  # Open valve for the specified duration in seconds

        while valve_control.IsValveOpen():
            time.sleep(0.1)  # Check every 0.1 seconds

        print(f"Valve on pin {pin} closed.")
        time.sleep(1)  # Short delay between iterations

# Function to handle calibration in a separate thread
def start_calibration(pin, duration_ms):
    thread = Thread(target=calibrate_valve, args=(pin, duration_ms, arduino))
    thread.start()

# Initialize the ArduinoDigital object
comport = "COM11"
arduino = ArduinoDigital(comport)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Valve Calibration")

# Creating input fields for pin number and duration
pin_label = tk.Label(root, text="Enter Pin Number:")
pin_label.pack()
pin_entry = tk.Entry(root)
pin_entry.pack()

duration_label = tk.Label(root, text="Enter Duration (ms):")
duration_label.pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

# Button to start calibration
calibrate_button = tk.Button(root, text="Start Calibration",
                             command=lambda: start_calibration(int(pin_entry.get()),
                                                               int(duration_entry.get())))
calibrate_button.pack()

# Start the GUI event loop
root.mainloop()
