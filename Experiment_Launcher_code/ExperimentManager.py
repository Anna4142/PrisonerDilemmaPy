
from Sound_manager_code.SoundManager import Play, Sounds
from modelling_opponent.MouseMonitor import Locations
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Data_analysis.logger import TrialLogger
from Data_analysis.event_logger import EventLogger
from Experiment_Launcher_code.RunTimeGui import RunTimeGUI
import time


class ExperimentManager:
    def __init__(self, video_analyzer, reward_manager):
        # initialize software components
        self.reward_manager = reward_manager
        self.videoAnalyser = video_analyzer
        self.stateManager = StateManager()
        self.trial_logger = TrialLogger()
        self.event_logger = EventLogger()
        self.runTimeGui = None

        # Set default reward and punishment times
        self.reward_time = 0.15
        self.sucker_time = 0
        self.temptation_time = 0.3
        self.punishment_time = 0.075
        self.center_reward_time = 0.02

        # initialize experiment control variables
        self.numcompletedtrial = 0
        self.time_start = time.time()
        self.time_to_make_decision = 0
        self.time_to_return_to_center = 0
        self.opponent_choice=0
        self.mouse_choice=0
        self.mouse_reward=0
        self.mouse_center_reward=0
        self.opponent_reward=0
        self.opponent_center_reward=0
        self.time_start=0
        self.time_to_make_decision=0
        self.time_to_return_to_center=0
        self.termination_parameter = 0
        self.termination_condition = None
        self.currentstate = None
        self.state_history = []
        self.sessionStartTime = 0
        self.mouse1 = None
        self.mouse2 = None
        self.decisionTimeout = False
        self.returnTimeout = False

        self.timestamps={}  ##for the video writer
        self.userStop = False
        self.state_start_times = {}  # Dictionary to store start times for each state

    def stopExperiment(self):
        self.userStop = True

    def start_state_timer(self, state):
        self.state_start_times[state] = time.time()

    def get_state_duration(self, state):
        return time.time() - self.state_start_times.get(state, time.time())

    def StateActivity(self, state, mouse1, mouse2):
        if state == States.Start:
            self.visit_cen = False
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.CenterReward:
            print(self.timestamps)
            self.visit_cen = True
            print("delivering reward in the center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time)
            mouse2.DeliverReward(Locations.Center, self.center_reward_time)
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.TrialStarted:
            Play(Sounds.Start)
            if self.numcompletedtrial > 0:
                self.time_to_return_to_center = time.time() - self.start_return_time
                self.trial_logger.log_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice,
                                       self.mouse_choice, self.mouse_reward, self.mouse_center_reward,
                                       self.opponent_reward, self.opponent_center_reward,
                                       self.time_start, self.time_to_make_decision, self.time_to_return_to_center)

            self.time_to_make_decision = 0
            self.time_to_return_to_center = 0
            self.time_start = time.time()
            mouse1.NewTrial()
            mouse2.NewTrial()
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "0.012"
            self.opponent_reward = "0.012"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Cooperate, self.reward_time)
            mouse2.DeliverReward(Locations.Cooperate, self.reward_time)
            self.time_to_make_decision = time.time() - self.time_start
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0"
            self.opponent_reward = "0.024"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Defect, self.sucker_time)
            mouse2.DeliverReward(Locations.Cooperate, self.temptation_time)
            self.time_to_make_decision = time.time() - self.time_start
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward = "0.024"
            self.opponent_reward = "0"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Cooperate, self.temptation_time)
            mouse2.DeliverReward(Locations.Defect, self.sucker_time)
            self.time_to_make_decision = time.time() - self.time_start
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.M1DM2D:
            # Actions for M1DM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "0.006"
            self.opponent_reward = "0.006"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Defect, self.punishment_time)
            mouse2.DeliverReward(Locations.Defect, self.punishment_time)
            self.time_to_make_decision = time.time() - self.time_start
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            self.start_return_time = time.time()

            self.timestamps = {
                'Start Time': self.time_start,
                'Decision Time': self.time_to_make_decision,
                'Return Time': self.time_to_return_to_center
            }
            if self.visit_cen == True:
                self.mouse_center_reward = "0.002"
                self.opponent_center_reward = "0.002"
            else:
                self.mouse_center_reward = "0.00"
                self.opponent_center_reward = "0.00"

            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

            # Update run time GUI
            self.runTimeGui.UpdateTrialDisplay(self.numcompletedtrial)
            self.runTimeGui.updateDecisionHistory(self.numcompletedtrial, 1, self.mouse_choice)
            self.runTimeGui.updateDecisionHistory(self.numcompletedtrial, 2, self.opponent_choice)
            self.runTimeGui.updateTimeoutHistory(self.numcompletedtrial, 1, self.returnTimeout, self.decisionTimeout)
            self.returnTimeout = False
            self.decisionTimeout = False

        elif state == States.ReturnTimeOut:
            Play(Sounds.Abort)
            print("Trial has been aborted.")
            self.returnTimeout = True
            self.opponent_center_reward = "0.00"
            self.mouse_center_reward = "0.00"
            self.start_return_time = time.time()
            self.trial_logger.log_data(self.numcompletedtrial, "DIDNT RETURN TO CENTER", self.opponent_choice,
                                       self.mouse_choice, self.mouse_reward, self.mouse_center_reward,
                                       self.opponent_reward, self.opponent_center_reward,
                                       self.time_start, self.time_to_make_decision, self.time_to_return_to_center)
            self.visit_cen == False
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.DecisionTimeOut:
            Play(Sounds.Abort)
            mouse1.DecisionAbort()
            mouse2.DecisionAbort()
            print("IN DECISION ABORT")
            self.decisionTimeout = True
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "0.00"
            self.opponent_reward = "0.00"
            self.opponent_center_reward = "0.00"
            self.mouse_center_reward = "0.00"
            self.start_return_time = time.time()

            self.trial_logger.log_data(self.numcompletedtrial, "DIDNT MAKE DECISION", self.opponent_choice,
                                       self.mouse_choice, self.mouse_reward, self.mouse_center_reward,
                                       self.opponent_reward, self.opponent_center_reward,
                                       self.time_start, self.time_to_make_decision, self.time_to_return_to_center)
            self.event_logger.log_data(self.numcompletedtrial, state, time.time())

        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.

            self.event_logger.log_data(self.numcompletedtrial, state, time.time())
            self.trial_logger.finalize_logging()
            self.event_logger.finalize_logging()

    def start_streaming_exp(self, experiment_parameters, mouse1, mouse2):
        self.trial_logger.start_logging()
        self.event_logger.start_logging()
        self.termination_condition = experiment_parameters.get("termination_type")
        self.termination_parameter = experiment_parameters.get("termination_value")
        if self.termination_condition == "Minutes":
            self.termination_parameter *= 60    # convert to seconds
        self.stateManager.SetTimeOut(experiment_parameters.get("decision_time"), experiment_parameters.get("return_time"))
        self.mouse1 = mouse1
        self.mouse2 = mouse2

        #setup run time GUI
        self.runTimeGui = RunTimeGUI()
        self.sessionStartTime = time.time()
        self.runTimeGui.StartMonitoring(self.experimentControl, self.stopExperiment)

    def experimentControl(self):
        experimentended = False
        self.runTimeGui.UpdateTimeDisplay(time.time() - self.sessionStartTime)
        if self.currentstate != States.End:
            trialevents = self.checkTerminationEvenets()

            if self.reward_manager.is_reward_delivered():
                trialevents += Events.RewardDelivered.value

            zone_activations = self.videoAnalyser.process_single_frame(self.timestamps)
            # print("zone activations", zone_activations)  ##just for debugging purposes

            first_opponent_choice = self.mouse1.getDecision(zone_activations)
            Second_opponent_choice = self.mouse2.getDecision(zone_activations)

            if first_opponent_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse1InCenter.value
            elif first_opponent_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse1Cooporated.value
            elif first_opponent_choice == Locations.Defect:
                trialevents = trialevents + Events.Mouse1Defected.value

            if Second_opponent_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse2InCenter.value
            elif Second_opponent_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse2Cooporated.value
            elif Second_opponent_choice == Locations.Defect:
                trialevents = trialevents + Events.Mouse2Defected.value

            nextstate = self.stateManager.DetermineState(trialevents)

            if nextstate != self.currentstate:
                self.currentstate = nextstate
                print(f"Current State: {self.currentstate}")
                self.state_history.append(self.currentstate)
                self.StateActivity(self.currentstate, self.mouse1, self.mouse2)

        else:    # Experiment terminated
            experimentended = True

        return experimentended

    def checkTerminationEvenets(self):
        trialevents = 0

        if self.userStop:
            trialevents = Events.ExperimentStopped.value

        if self.termination_condition == 'Minutes':
            if time.time() - self.sessionStartTime > self.termination_parameter:
                trialevents = Events.ExperimentStopped.value
        else:
            if self.numcompletedtrial == self.termination_parameter:
                trialevents += Events.LastTrial.value

        return trialevents