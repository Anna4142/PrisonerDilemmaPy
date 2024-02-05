# Assuming you have a class or module ArduinoDigital with the relevant methods
import Arduino_related_code.ArduinoDigital as Arduino
from Arduino_related_code.ValveControl import ValveControl
import time

# Initialize the ArduinoDigital object
comport = "COM11"
Arduino.openComPort(comport)

# Initialize ValveControl for a specific channel
valve_control = ValveControl(11)  # Assume pin 8 for the valve

for i in range(100):
    print(f"Opening valve.")
    valve_control.OpenValve(0.02)  # Open valve for 2 seconds

    # Wait until the valve is closed
    while valve_control.IsValveOpen():
        time.sleep(0.02)  # Check every 0.1 seconds

    print(f"Valve closed .")
     # Optional: a short delay before the next iteration
