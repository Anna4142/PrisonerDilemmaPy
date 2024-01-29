import serial

global comport;

def openComPort(portname):
    comport = serial.Serial(portname, 9600)

def DigitalHigh(pin):
    sendMessage('E', pin, 1, 0);

def DigitalLow(self, pin):
    sendMessage('E', pin, 0, 0);

def DigitalHighPulse(pin, width):
    sendMessage('P', pin, 1, width);

def DigitalLowPulse(pin, width):
    sendMessage('P', pin, 0, width);

def sendMessage(command, pin, polarity, width):
    outbyte = command.to_bytes(1, 'big')
    comport.write(outbyte)
    outbyte = pin.to_bytes(1, 'big')
    comport.write(outbyte)
    outbyte = polarity.to_bytes(1, 'big')
    comport.write(outbyte)
    outbyte = width.to_bytes(2, 'big')
    comport.write(outbyte)
