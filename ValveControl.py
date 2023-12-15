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
        #print(self.arduino.DigitalHigh(self.channel))     # Micky: I hope this is not something I did :-)
                                                          #        why printing the return value of a function that does not return any value?
        self.valveopen = True

    def IsValveOpen(self):
        if self.valveopen:
            if time.time() - self.starttime > self.duration:
                #print("delivered")                        # Micky: I think this print is not needed.
                                                          #        The the function with the arduinoSim. you get enough printouts from these functions.
                                                          #        once you move to the real system you know you you can trust the code.
                self.arduino.DigitalLow(self.channel)  # Set the pin low
                self.valveopen = False
        return self.valveopen
