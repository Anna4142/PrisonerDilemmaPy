import time

class ValveControl:
    def __init__(self, channel, arduino):
        self.channel = channel
        self.arduino = arduino  # This is an instance of ArduinoDigital
        self.CloseValve()
        self.starttime = 0
        self.duration = 0
        self.valveopen = False

    def OpenValve(self, duration):
        if duration > 0:
            self.starttime = time.time()
            self.duration = duration
            self.arduino.DigitalLow(self.channel)  # Set the pin low
            self.valveopen = True

    def CloseValve(self):
        self.arduino.DigitalHigh(self.channel)  # Set the pin high
        self.valveopen = False

    def IsValveOpen(self):
        if self.valveopen:
            if time.time() - self.starttime > self.duration:
                self.CloseValve()
        return self.valveopen
