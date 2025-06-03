import serial
import time

global comport

def openComPort(portname):
    global comport
    comport = serial.Serial(portname, 9600)
    print(portname)
    time.sleep(0.05)# Arduino resets itself when the port is opened. Give it time to complete.

def DigitalHigh(pin):
    sendMessage('E', pin, 1, 0)

def DigitalLow(pin):
    sendMessage('E', pin, 0, 0)

def DigitalHighPulse(pin, width):
    sendMessage('P', pin, 1, width)

def DigitalLowPulse(pin, width):
    sendMessage('P', pin, 0, width)

def sendMessage(command, pin, polarity, width):
    outbyte = ord(command).to_bytes(1, 'big')
    serialout(outbyte)
    outbyte = pin.to_bytes(1, 'big')
    serialout(outbyte)
    outbyte = polarity.to_bytes(1, 'big')
    serialout(outbyte)
    outbyte = width.to_bytes(2, 'big')
    serialout(outbyte)

def serialout(outbyte):
    if not comport.isOpen():
        print('Arduino Com port is not open')

    '''
    try:
        numbytes = comport.out_waiting
        if numbytes > 0:
            print(f'Arduino out buffer not empty ({numbytes})')
    except Exception as e:
        print (f'check buffer error {e}')
    '''

    try:
        comport.write(outbyte)
        time.sleep(0.001)
    except Exception  as e:
        print (f'Serial port exception: {e}')
        raise Exception('Serial port crash, restart program')


