from Sound_manager_code.SoundManager import Play, Sounds
from modelling_opponent.MouseMonitor import Locations
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Data_analysis.logger import TrialLogger
from Data_analysis.event_logger import EventLogger
from Experiment_Launcher_code.RunTimeGui import RunTimeGUI
import Data_analysis.CodeProfiler as Profiler
from Data_analysis.RunTimeAnalysis import RunTimeAnalysis
from Data_analysis.HeartBeat import HeartBeat
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
        self.run_time_analysis = RunTimeAnalysis(30, 2, 60)
        self.heartbeat = HeartBeat(4, 30)

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
        self.session_progress_percent = 0

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
            print("delivering reward in the center ")
            mouse1.DeliverReward(Locations.Center, 'CN')
            mouse2.DeliverReward(Locations.Center, 'CN')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.TrialStarted:
            if self.trial_number > 0:
                if self.mouse1_return_time == 0:
                    mouse1_status = self.trial_status
                    self.mouse1_return_time = time.time() - self.start_return_timer
                else:
                    mouse1_status = 'Completed'
                if self.mouse2_return_time == 0:
                    mouse2_status = self.trial_status
                    self.mouse2_return_time = time.time() - self.start_return_timer
                else:
                    mouse2_status = 'Completed'
                self.trial_logger_1.log_data(self.trial_number, mouse1_status, self.mouse1_choice,
                                             self.mouse2_choice, self.mouse1_reward, self.mouse1_center_reward,
                                             self.trial_start_time - self.sessionStartTime, self.mouse1_decision_time, self.mouse1_return_time)
                self.trial_logger_2.log_data(self.trial_number, mouse2_status, self.mouse2_choice,
                                             self.mouse1_choice, self.mouse2_reward, self.mouse2_center_reward,
                                             self.trial_start_time - self.sessionStartTime, self.mouse2_decision_time, self.mouse2_return_time)

            self.trial_number += 1
            self.run_time_analysis.new_trial()
            self.trial_start_time = time.time()
            self.trial_status = 'Incomplete'
            mouse1.NewTrial()
            mouse2.NewTrial()

            Play(Sounds.Start)

            self.mouse1_decision_time = 0
            self.mouse1_return_time = 0
            self.mouse1_choice = 'N/A'
            self.mouse1_reward = 'N/A'
            self.mouse1_center_reward = '0'

            self.mouse2_decision_time = 0
            self.mouse2_return_time = 0
            self.mouse2_choice = 'N/A'
            self.mouse2_reward = 'N/A'
            self.mouse2_center_reward = '0'

            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.mouse1_choice = "C"
            self.mouse2_choice = "C"
            self.mouse1_reward = self.reward_manager.get_reward(1, 'CC')
            self.mouse2_reward = self.reward_manager.get_reward(2, 'CC')
            #self.mouse1_center_reward = "0"
            #self.mouse2_center_reward = "0"
            mouse1.DeliverReward(Locations.Cooperate, 'CC')
            mouse2.DeliverReward(Locations.Cooperate, 'CC')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse1_decision_time = time.time() - self.trial_start_time
            self.mouse2_decision_time = time.time() - self.trial_start_time
            self.mouse1_choice = "C"
            self.mouse2_choice = "D"
            self.mouse1_reward = self.reward_manager.get_reward(1, 'CD')
            self.mouse2_reward = self.reward_manager.get_reward(2, 'CD')
            #self.mouse1_center_reward = "0"
            #self.mouse2_center_reward = "0"
            mouse1.DeliverReward(Locations.Defect, 'CD')
            mouse2.DeliverReward(Locations.Cooperate, 'CD')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            mouse1.DeliverReward(Locations.Cooperate, 'DC')
            mouse2.DeliverReward(Locations.Defect, 'DC')
            self.mouse1_choice = "D"
            self.mouse2_choice = "C"
            self.mouse1_reward = self.reward_manager.get_reward(1, 'DC')
            self.mouse2_reward = self.reward_manager.get_reward(2, 'DC')
            #self.mouse1_center_reward = "0"
            #self.mouse2_center_reward = "0"
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
            self.mouse1_reward = self.reward_manager.get_reward(1, 'DD')
            self.mouse2_reward = self.reward_manager.get_reward(2, 'DD')
            #self.mouse1_center_reward = "0"
            #self.mouse2_center_reward = "0"
            mouse1.DeliverReward(Locations.Defect, 'DD')
            mouse2.DeliverReward(Locations.Defect, 'DD')
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
            self.mouse1_center_reward = self.reward_manager.get_reward(1, 'CN')
            self.stateManager.SetVariableTimeOut(self.return_max_time - self.mouse1_return_time)
            print("Delivering reward in M1 center ")
            mouse1.DeliverReward(Locations.Center, 'CN')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M2SecondInCenter:
            self.mouse2_return_time = time.time() - self.start_return_timer
            self.mouse2_center_reward = self.reward_manager.get_reward(2, 'CN')
            print("Delivering reward in M2 center ")
            mouse2.DeliverReward(Locations.Center, 'CN')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse2_last_location, time.time() - self.sessionStartTime)

        elif state == States.M2FirstInCenter:
            self.mouse2_return_time = time.time() - self.start_return_timer
            self.mouse2_center_reward = self.reward_manager.get_reward(2, 'CN')
            self.stateManager.SetVariableTimeOut(self.return_max_time - self.mouse2_return_time)
            print("Delivering reward in M2 center ")
            mouse2.DeliverReward(Locations.Center, 'CN')
            self.event_logger_1.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)
            self.event_logger_2.log_data("State", self.trial_number, state, self.mouse1_last_location, time.time() - self.sessionStartTime)

        elif state == States.M1SecondInCenter:
            self.mouse1_return_time = time.time() - self.start_return_timer
            self.mouse1_center_reward = self.reward_manager.get_reward(1, 'CN')
            print("Delivering reward in M1 center ")
            mouse1.DeliverReward(Locations.Center, 'CN')
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
            self.heartbeat.stop()

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

        # setup run time GUI and Event Analyser
        self.runTimeGui = RunTimeGUI()
        self.sessionStartTime = time.time()
        self.videoAnalyser.start_video()
        self.heartbeat.start(self.sessionStartTime)
        self.runTimeGui.StartMonitoring(self.experimentControl, self.stopExperiment)
        self.run_time_analysis.reset_analysis_timers()

    def experimentControl(self):
        Profiler.EnterMainLoop()
        experimentended = False

        Profiler.EnterFunction('Run Time GUI')
        self.runTimeGui.UpdateTimeDisplay(time.time() - self.sessionStartTime)
        Profiler.ExitFunction('Run Time GUI')

        if self.currentstate != States.End:
            trialevents = self.checkTerminationEvenets()
            session_progress = self.calculateSessionProgress()
            if session_progress - self.session_progress_percent > 1:
                self.session_progress_percent = session_progress
                self.runTimeGui.UpdateProgress(session_progress)

            if self.reward_manager.is_reward_delivered():
                trialevents += Events.RewardDelivered.value

            Profiler.EnterFunction('Process Single Frame')
            zone_activations = self.videoAnalyser.process_single_frame()

            # print("zone activations", zone_activations)  ##just for debugging purposes
            Profiler.ExitFunction('Process Single Frame')

            mouse1_choice = self.mouse1.getDecision(zone_activations)
            mouse2_choice = self.mouse2.getDecision(zone_activations)
            if mouse1_choice != self.mouse1_last_location:
                self.mouse1_last_location = mouse1_choice
                self.event_logger_1.log_data('Location', self.trial_number, self.currentstate, mouse1_choice, time.time() - self.sessionStartTime)
                self.run_time_analysis.new_mouse_position(1)
            if mouse2_choice != self.mouse2_last_location:
                self.mouse2_last_location = mouse2_choice
                self.event_logger_2.log_data('Location', self.trial_number, self.currentstate, mouse2_choice, time.time() - self.sessionStartTime)
                self.run_time_analysis.new_mouse_position(2)

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


            self.heartbeat.generate_heartbeat(self.videoAnalyser.get_dropped_frames())

            self.run_time_analysis.event_analysis(self.runTimeGui.UpdateEventLog)
            Profiler.EnterFunction('Determine State')
            nextstate = self.stateManager.DetermineState(trialevents)
            Profiler.ExitFunction('Determine State')

            if nextstate != self.currentstate:
                self.currentstate = nextstate
                print(f"Current State: {self.currentstate}")
                self.state_history.append(self.currentstate)
                Profiler.EnterFunction('State Activity')
                self.StateActivity(self.currentstate, self.mouse1, self.mouse2)
                Profiler.ExitFunction('State Activity')

        else:    # Experiment terminated
            experimentended = True
            print(f' Total number of dropped frames= {self.videoAnalyser.get_dropped_frames()}')

        Profiler.ExitMainLoop()
        return experimentended

    def calculateSessionProgress(self):
        if self.termination_condition == 'Minutes':
            percent = int((time.time() - self.sessionStartTime) / self.termination_parameter * 100)
        else:
            percent = int(self.trial_number / self.termination_parameter * 100)
        return percent

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
