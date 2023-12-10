import time
from ArduinoDigital import ArduinoDigital
class ValveControl:
    def __init__(self, channel, arduino):
        self.channel = channel
        self.arduino = arduino  # This is an instance of ArduinoDigital
        #self.arduino.DigitalLow(self.channel)  # Set the pin low initially
        self.starttime = 0
        self.duration = 0
        self.valveopen = False

    def OpenValve(self, duration):

        self.starttime = time.time()
        self.duration = duration
        self.arduino.DigitalHigh(self.channel)  # Set the pin high
        print(self.arduino.DigitalHigh(self.channel))
        self.valveopen = True

    def IsValveOpen(self):
        if self.valveopen:
            if time.time() - self.starttime > self.duration:
                print("delivered")
                self.arduino.DigitalLow(self.channel)  # Set the pin low
                self.valveopen = False
        return self.valveopen
