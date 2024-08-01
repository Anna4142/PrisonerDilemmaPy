import serial
import time

global comport;

def openComPort(portname):
    global comport;
    comport = serial.Serial(portname, 9600)
    print(portname)
    time.sleep(0.05)# Arduino resets itself when the port is opened. Give it time to complete.

def DigitalHigh(pin):
    sendMessage('E', pin, 1, 0);

def DigitalLow(pin):
    sendMessage('E', pin, 0, 0);

def DigitalHighPulse(pin, width):
    sendMessage('P', pin, 1, width);

def DigitalLowPulse(pin, width):
    sendMessage('P', pin, 0, width);

def sendMessage(command, pin, polarity, width):
    outbyte = ord(command).to_bytes(1, 'big')
    comport.write(outbyte)
    time.sleep(0.01)
    print("writing high")
    outbyte = pin.to_bytes(1, 'big')
    comport.write(outbyte)
    time.sleep(0.01)
    outbyte = polarity.to_bytes(1, 'big')
    comport.write(outbyte)
    time.sleep(0.01)
    outbyte = width.to_bytes(2, 'big')
    comport.write(outbyte)
    time.sleep(0.01)

