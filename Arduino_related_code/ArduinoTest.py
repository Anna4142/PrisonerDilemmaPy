from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as arduino
else:
    import Arduino_related_code.ArduinoDigital as arduino

##### main
opcode = -1
arduino.openComPort("COM11");

while opcode != 0:
    opcodestr = input("opcode [0- exit, 1- Valve on, 2- Valve of, 3 - high pule, 4 - low pulse]: ")
    opcode = int(opcodestr)

    if opcode == 0:
        print("Program terminated")

    elif opcode == 1:
        pin = int(input("select valve: "))
        arduino.DigitalHigh(pin)

    elif opcode == 2:
        pin = int(input("select valve: "))
        arduino.DigitalLow(pin)

    else:
        print ("illegal opcode")
