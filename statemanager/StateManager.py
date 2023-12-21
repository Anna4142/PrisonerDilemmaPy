import time
from enum import Enum
import numpy as np

class States (Enum):
    Start               = 1
    CenterReward        = 2
    TrialStarted        = 3
    M1CM2C              = 4
    M1CM2D              = 5
    M1DM2C              = 6
    M1DM2D              = 7
    WaitForReturn       = 8
    TrialCompleted      = 9
    TrialAbort          = 10
    DecisionAbort       = 11
    End                 = 12

class Events (Enum):
    Mouse1InCenter   = 1
    Mouse2InCenter   = 2
    Mouse1Cooporated = 4
    Mouse2Cooporated = 8
    Mouse1Defected   = 16
    Mouse2Defected   = 32
    LastTrial        = 64
    RewardDelivered  = 128
class Locations(Enum):
    Unknown=0
    Center = 1
    Cooperate = 2
    Defect = 3
class StateManager:
    def __init__(self):
        self.NextState = {
            States.Start : [States.CenterReward],
            States.CenterReward : [States.TrialStarted],
            States.TrialStarted : [States.M1CM2C, States.M1CM2D, States.M1DM2C, States.M1DM2D],
            States.M1CM2C : [States.WaitForReturn],
            States.M1CM2D: [States.WaitForReturn],
            States.M1DM2C: [States.WaitForReturn],
            States.M1DM2D: [States.WaitForReturn],
            States.WaitForReturn:[States.TrialCompleted],
            States.TrialCompleted:[States.End],
            States.TrialAbort:[States.End, States.TrialStarted],
            States.DecisionAbort:[States.End],
            States.End:[States.End]
        }

        self.TransitionEvent = {
            States.Start : [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.CenterReward : [0],
            States.TrialStarted : [Events.Mouse1Cooporated.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Cooporated.value + Events.Mouse2Defected.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Defected.value],
            States.M1CM2C : [0],
            States.M1CM2D: [0],
            States.M1DM2C: [0],
            States.M1DM2D: [0],
            States.WaitForReturn:[Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.TrialCompleted:[Events.LastTrial.value],
            States.TrialAbort:[Events.LastTrial.value, Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.DecisionAbort:[Events.LastTrial.value],
            States.End:[0]
        }

        self.RewardCalculation = {
            States.Start: lambda action: 1 if action == Locations.Center else -1,
            States.CenterReward: lambda action: 1 if action == Locations.Center else -1,
            States.TrialStarted: lambda action: 1 if action == Locations.Center else -1,
            States.M1CM2C: lambda action: 3 if action == Locations.Cooperate else -1,
            States.M1CM2D: lambda action: -2 if action == Locations.Cooperate else 0,
            States.M1DM2C: lambda action: 5 if action == Locations.Defect else -1,
            States.M1DM2D: lambda action: 1 if action == Locations.Defect else -1,
            States.WaitForReturn: lambda _: 0,  # Neutral reward for WaitForReturn state
            States.TrialCompleted: lambda action: 1 if action == Locations.Center else -1,
            States.TrialAbort: lambda action: 1 if action == Locations.Center else -1,
            States.DecisionAbort: lambda action: 1 if action == Locations.Center else -1,
            States.End: lambda _: 0  # Neutral reward for End state
        }

        self.TimeOutState = {
            States.Start : None,
            States.CenterReward : None,
            States.TrialStarted : States.DecisionAbort,
            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: States.TrialAbort,
            States.TrialCompleted: States.CenterReward,
            States.TrialAbort: None,
            States.DecisionAbort: States.TrialStarted,
            States.End: None
        }

        # the time out setting are just defaults
        self.decision_time = 0
        self.return_time = 0

        self.TransitionTimeOut = {
            States.Start: None,
            States.CenterReward: None,
            States.TrialStarted: self.decision_time,
            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: self.return_time,
            States.TrialCompleted: 0,
            States.TrialAbort: None,
            States.DecisionAbort: 0,
            States.End: None
        }

        self.current_state = States.Start
        self.StateStartTime = time.time()

    def SetTimeOuts(self, decision_time, return_time):
        self.decision_time = decision_time
        self.return_time = return_time
    def get_state_size(self):
        return len(States)

    def get_action_size(self):
        return len(Locations)

    def get_state_enum(index):
        return States(index)

    def get_state_index(self,state_enum):
        return state_enum.value

    def get_current_state_as_numpy(self,state):
        # Create a NumPy array with one element: the integer value of the current state
        return np.array([state.value])

    def DetermineState(self, events):
        TransitionEvents = self.TransitionEvent[self.current_state]

        # Check and Perform Event base transition
        for i, event in enumerate(TransitionEvents):
            if event & events == event:
                # Transition to the next state based on the event
                self.current_state = self.NextState[self.current_state][i]
                self.StateStartTime = time.time()
                return self.current_state

        # Check and Perform timeout base transition
        if self.TimeOutState[self.current_state]:
            if time.time() - self.StateStartTime > self.TransitionTimeOut[self.current_state]:
                # Transition to the timeout state
                self.current_state = self.TimeOutState[self.current_state]
                self.StateStartTime = time.time()

        return self.current_state