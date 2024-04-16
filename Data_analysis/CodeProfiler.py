# this code profiler keeps track of frame rate and calculates the CPU usage of the 3 most
# time consuming functions. It does not handle nested functions. Time spent in nested function
# will be accrued both to the calling and nested function.

import time
import statistics


FunctionEntries = {}
FrameAveragePeriodStart = time.time()
FrameCounter = 0
FunctionStartTime = {}
FunctionName = []
FunctionTime = []


def NewFrame():
    global FrameCounter, FrameAveragePeriodStart
    global FunctionName, FunctionTime

    FrameCounter += 1
    period = time.time() - FrameAveragePeriodStart
    if period > 20:
        framerate = FrameCounter/period
        print(f'Frame Rate= : {framerate:.2f}')
        FrameAveragePeriodStart = time.time()
        FrameCounter = 0
        CalculateFunctionAverages(period)
        for index in range(len(FunctionTime)):
            if FunctionTime[index] > 0:
                print(f'CPU usage: {FunctionName[index]}, {FunctionTime[index]:.2e}%')

def EnterFunction(name):
    global FunctionStartTime

    if name in FunctionStartTime and FunctionStartTime[name] != 0:
        print(f'Code Profiler Error. Function {name} missing an exit point')
    else:
        FunctionStartTime[name] = time.time()

def ExitFunction(name):
    global FunctionStartTime, FunctionEntries

    if name in FunctionStartTime:
        functiontime = time.time() - FunctionStartTime[name]
        FunctionStartTime[name] = 0

        if not name in FunctionEntries:
            #FunctionEntries[name] = [functiontime]
            FunctionEntries[name] = []
        FunctionEntries[name].append(functiontime)
    else:
        print(f'Code Profiler Error. Function {name} missing an entry point')


def CalculateFunctionAverages(period):
    global FunctionEntries, CPUUsage
    global FunctionName, FunctionTime

    topcount = 3
    FunctionName = [''] * topcount
    FunctionTime = [0] * topcount

    for function in FunctionEntries:
        functionCpuTime = sum(FunctionEntries[function]) / period * 100
        for index in range(topcount):
            if functionCpuTime > FunctionTime[index]:
                for pushindex in range(topcount - 1, index, -1):
                    FunctionName[pushindex] = FunctionName[pushindex - 1]
                    FunctionTime[pushindex] = FunctionTime[pushindex - 1]
                FunctionName[index] = function
                FunctionTime[index] = functionCpuTime
                break

    FunctionEntries = {}

