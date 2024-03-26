from RunTimeGui import RunTimeGUI
import time
import random

#global runtimegui
def mainloop():
    global startTime, trialTime, trialNum, runtimegui, experimentEnded

    sessiontime = time.time() - startTime
    runtimegui.UpdateTimeDisplay(sessiontime)
    intrialtime = sessiontime - trialNum * 5

    if intrialtime > 5:
        trialNum += 1
        runtimegui.UpdateTrialDisplay(trialNum)
        trialSummery(1, trialNum)
        trialSummery(2, trialNum)

    return experimentEnded

def trialSummery(mouse, trialNum):
    centertimeout = False
    decisiontimout = False
    decision = 'C'
    if random.random() < 0.5:
        centertimeout = True
    if random.random() < 0.5:
        decisiontimout = True
    if random.random() < 0.5:
        decision = 'D'
    runtimegui.updateDecisionHistory(trialNum, mouse, decision)
    runtimegui.updateTimeoutHistory(trialNum, mouse, centertimeout, decisiontimout)

def stopexperiment():
    global experimentEnded
    experimentEnded = True


# main
runtimegui = RunTimeGUI()
startTime = time.time()
trialNum = 0
experimentEnded = False
runtimegui.StartMonitoring(mainloop, stopexperiment)
