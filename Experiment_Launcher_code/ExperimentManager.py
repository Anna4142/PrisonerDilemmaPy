
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
        self.trial_logger_1 = TrialLogger(1)
        self.trial_logger_2 = TrialLogger(2)
        self.event_logger_1 = EventLogger(1)
        self.event_logger_2 = EventLogger(2)
        self.runTimeGui = None

        # Set default reward and punishment times
        self.reward_time = [0.108, 0.114]
        self.sucker_time = [0, 0]
        self.temptation_time = [0.248, 0.144]
        self.punishment_time = [0.047, 0.027]
        self.center_reward_time = [0.02, 0.019]

        # initialize experiment control variables
        self.trial_number = 0
        self.trial_start_time = time.time()
        self.termination_parameter = 0
        self.termination_condition = None
        self.currentstate = None
        self.state_history = []
        self.sessionStartTime = 0
        self.mouse1 = None
        self.mouse2 = None
        self.return_max_time = 0
        self.trial_status = 'Incomplete'
        self.start_return_timer = 0

        self.timestamps = {}  # for the video writer
        self.userStop = False
        self.state_start_times = {}  # Dictionary to store start times for each state

        self.mouse1_decision_time = 0
        self.mouse1_return_time = 0
        self.mouse1_choice = "N/A"
        self.mouse1_reward = 0
        self.mouse1_center_reward = 0
        self.mouse1_last_location = None

        self.mouse2_decision_time = 0
        self.mouse2_return_time = 0
        self.mouse2_choice = "N/A"
        self.mouse2_reward = 0
        self.mouse2_center_reward = 0
        self.mouse2_last_location = None

    def stopExperiment(self):
        self.userStop = True

    def start_state_timer(self, state):
        self.state_start_times[state] = time.time()

    def get_state_duration(self, state):
        return time.time() - self.state_start_times.get(state, time.time())

    def StateActivity(self, state, mouse1, mouse2):
        if state == States.Start:
            # self.visit_cen = False
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.CenterReward:
            print(self.timestamps)
            # self.visit_cen = True
            print("delivering reward in the center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time[0])
            mouse2.DeliverReward(Locations.Center, self.center_reward_time[1])
            #if self.trial_number > 0:
            #    self.mouse1_return_time = time.time() - self.start_return_timer
            #    self.mouse2_return_time = time.time() - self.start_return_timer
            #    self.mouse1_center_reward = "0.002"
            #    self.mouse2_center_reward = "0.002"
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.TrialStarted:
            if self.trial_number > 0:
                if self.mouse1_return_time == 0:
                    self.mouse1_return_time = time.time() - self.start_return_timer
                if self.mouse2_return_time == 0:
                    self.mouse2_return_time = time.time() - self.start_return_timer
                self.trial_logger_1.log_data(self.trial_number, self.trial_status, self.mouse1_choice,
                                             self.mouse2_choice, self.mouse1_reward, self.mouse1_center_reward,
                                             self.trial_start_time - self.sessionStartTime, self.mouse1_decision_time, self.mouse1_return_time)
                self.trial_logger_2.log_data(self.trial_number, self.trial_status, self.mouse2_choice,
                                             self.mouse1_choice, self.mouse2_reward, self.mouse2_center_reward,
                                             self.trial_start_time - self.sessionStartTime, self.mouse2_decision_time, self.mouse2_return_time)

            self.trial_number += 1
            self.trial_start_time = time.time()
            self.trial_status = 'Incomplete'
            mouse1.NewTrial()
            mouse2.NewTrial()

            Play(Sounds.Start)

            self.mouse1_decision_time = 0
            self.mouse1_return_time = 0
            self.mouse1_choice = "N/A"
            self.mouse1_reward = 0
            self.mouse1_center_reward = 0

            self.mouse2_decision_time = 0
            self.mouse2_return_time = 0
            self.mouse2_choice = "N/A"
            self.mouse2_reward = 0
            self.mouse2_center_reward = 0

            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.mouse1_choice = "C"
            self.mouse2_choice = "C"
            self.mouse1_reward = "0.012"
            self.mouse2_reward = "0.012"
            self.mouse1_center_reward = "0.0"
            self.mouse2_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Cooperate, self.reward_time[0])
            mouse2.DeliverReward(Locations.Cooperate, self.reward_time[1])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.mouse1_choice = "C"
            self.mouse2_choice = "D"
            self.mouse1_reward = "0"
            self.mouse2_reward = "0.016"
            self.mouse1_center_reward = "0.0"
            self.mouse2_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Defect, self.sucker_time[0])
            mouse2.DeliverReward(Locations.Cooperate, self.temptation_time[1])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            mouse1.DeliverReward(Locations.Cooperate, self.temptation_time[0])
            mouse2.DeliverReward(Locations.Defect, self.sucker_time[1])
            self.mouse1_choice = "D"
            self.mouse2_choice = "C"
            self.mouse1_reward = "0.016"
            self.mouse2_reward = "0"
            self.mouse1_center_reward = "0.0"
            self.mouse2_center_reward = "0.0"
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1DM2D:
            # Actions for M1DM2D state
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.mouse1_choice = "D"
            self.mouse2_choice = "D"
            self.mouse1_reward = "0.003"
            self.mouse2_reward = "0.003"
            self.mouse1_center_reward = "0.0"
            self.mouse2_center_reward = "0.0"
            mouse1.DeliverReward(Locations.Defect, self.punishment_time[0])
            mouse2.DeliverReward(Locations.Defect, self.punishment_time[1])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.trial_status = 'Completed'
            self.start_return_timer = time.time()

            self.timestamps = {
                'Start Time': self.trial_start_time,
                'Decision Time': self.mouse1_decision_time,
                'Return Time': self.mouse1_return_time
            }

            print("Trial Completed. Number of completed trials: ", self.trial_number)
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

            # Update run time GUI
            self.runTimeGui.UpdateTrialDisplay(self.trial_number)
            self.runTimeGui.updateDecisionHistory(self.trial_number, 1, self.mouse1_choice)
            self.runTimeGui.updateDecisionHistory(self.trial_number, 2, self.mouse2_choice)

        elif state == States.M1FirstInCenter:
            self.mouse1_return_time = time.time() - self.start_return_timer
            self.mouse1_center_reward = "0.002"
            self.stateManager.SetVariableTimeOut(self.return_max_time - self.mouse1_return_time)
            print("Delivering reward in M1 center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time[0])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M2SecondInCenter:
            self.mouse2_return_time = time.time() - self.start_return_timer
            self.mouse2_center_reward = "0.002"
            print("Delivering reward in M2 center ")
            mouse2.DeliverReward(Locations.Center, self.center_reward_time[1])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M2FirstInCenter:
            self.mouse2_return_time = time.time() - self.start_return_timer
            self.mouse2_center_reward = "0.002"
            self.stateManager.SetVariableTimeOut(self.return_max_time - self.mouse2_return_time)
            print("Delivering reward in M2 center ")
            mouse2.DeliverReward(Locations.Center, self.center_reward_time[1])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1SecondInCenter:
            self.mouse1_return_time = time.time() - self.start_return_timer
            self.mouse1_center_reward = "0.002"
            print("Delivering reward in M1 center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time[0])
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.ReturnTimeOut:
            if self.mouse1_return_time == 0:
                self.runTimeGui.updateTimeoutHistory(self.trial_number, 1, True, False)
            if self.mouse2_return_time == 0:
                self.runTimeGui.updateTimeoutHistory(self.trial_number, 2, True, False)
            print("Trial has been aborted.")
            self.trial_status = 'Return Timeout'
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)
            Play(Sounds.Abort)

        elif state == States.DecisionTimeOut:
            Play(Sounds.Abort)
            mouse1.DecisionAbort()
            mouse2.DecisionAbort()
            print("IN DECISION ABORT")
            self.trial_status = 'Decision Timeout'
            self.runTimeGui.updateTimeoutHistory(self.trial_number, 1, False, True)
            self.runTimeGui.updateTimeoutHistory(self.trial_number, 2, False, True)
            self.start_return_timer = time.time()
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            self.trial_logger_1.log_data(self.trial_number, self.trial_status, self.mouse1_choice,
                                         self.mouse2_choice, self.mouse1_reward, self.mouse1_center_reward,
                                         self.trial_start_time - self.sessionStartTime, self.mouse1_decision_time, self.mouse1_return_time)
            self.trial_logger_2.log_data(self.trial_number, self.trial_status, self.mouse2_choice,
                                         self.mouse1_choice, self.mouse2_reward, self.mouse2_center_reward,
                                         self.trial_start_time - self.sessionStartTime, self.mouse2_decision_time, self.mouse2_return_time)
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)
            self.trial_logger_1.finalize_logging()
            self.trial_logger_2.finalize_logging()
            self.event_logger_1.finalize_logging()
            self.event_logger_2.finalize_logging()

    def start_streaming_exp(self, experiment_parameters, mouse1, mouse2):
        self.trial_logger_1.start_logging()
        self.trial_logger_2.start_logging()
        self.event_logger_1.start_logging()
        self.event_logger_2.start_logging()
        self.termination_condition = experiment_parameters.get("termination_type")
        self.termination_parameter = experiment_parameters.get("termination_value")
        if self.termination_condition == "Minutes":
            self.termination_parameter *= 60    # convert to seconds
        self.stateManager.SetFixedTimeOut(experiment_parameters.get("decision_time"), experiment_parameters.get("return_time"))
        self.return_max_time = experiment_parameters.get("return_time")
        self.mouse1 = mouse1
        self.mouse2 = mouse2

        # setup run time GUI
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
            #print("zone activations", zone_activations)  ##just for debugging purposes

            mouse1_choice = self.mouse1.getDecision(zone_activations)
            mouse2_choice = self.mouse2.getDecision(zone_activations)
            if mouse1_choice != self.mouse1_last_location:
                self.mouse1_last_location = mouse1_choice
                self.event_logger_1.log_data('Location', self.trial_number, self.currentstate, mouse1_choice, time.time() - self.sessionStartTime)
            if mouse2_choice != self.mouse2_last_location:
                self.mouse2_last_location = mouse2_choice
                self.event_logger_2.log_data('Location', self.trial_number, self.currentstate, mouse2_choice, time.time() - self.sessionStartTime)

            if mouse1_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse1InCenter.value
            elif mouse1_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse1Cooporated.value
            elif mouse1_choice == Locations.Defect:
                trialevents = trialevents + Events.Mouse1Defected.value

            if mouse2_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse2InCenter.value
            elif mouse2_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse2Cooporated.value
            elif mouse2_choice == Locations.Defect:
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
            if self.trial_number >= self.termination_parameter:
                trialevents += Events.LastTrial.value

        return trialevents