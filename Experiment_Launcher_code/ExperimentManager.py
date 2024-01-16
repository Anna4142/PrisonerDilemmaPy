
from Sound_manager_code.SoundManager import Play, Sounds
from modelling_opponent.MouseMonitor import Locations
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Data_analysis.logger import TrialLogger
from Data_analysis.event_logger import EventLogger
from Data_analysis.DataAnalysisScript import DataAnalyzer
from modelling_opponent.OpponentType import OpponentType
from Reward_manager.RewardManager import RewardManager
import time
from pynput.keyboard import Key, Listener
from threading import Lock


class ExperimentManager:
    def __init__(self, video_analyzer, reward_manager):
        # initialize software components
        self.reward_manager = reward_manager
        self.videoAnalyser = video_analyzer
        self.stateManager = StateManager()
        self.trial_logger = TrialLogger()

        self.event_logger = EventLogger()
        #self.data_analyzer = DataAnalyzer(self.trial_logger)

        #initialize reward manager

        self.opponent_type = ""  ##for the logger

        # Set default reward and punishment times
        self.reward_time = 0.2
        self.sucker_time = 0
        self.temptation_time = 0.4
        self.punishment_time = 0.1
        self.center_reward_time = 0.02

        # initialize experiment control variables
        self.numcompletedtrial = 0
        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0
        self.time_start = time.time()
        self.time_to_make_decision = 0
        self.time_to_return_to_center = 0

        self.timestamps={}##for the video writer
        self.event_lock = Lock()
        self.trialevents=0
        self.state_start_times = {}  # Dictionary to store start times for each state





    def on_press(self, key):
            with self.event_lock:
                if key == Key.esc:
                    print("Experiment stopped by user.")
                    self.trialevents = Events.ExperimentStopped.value
                    print("Trial events ending", self.trialevents)



    def on_release(self, key):
        print(f"Key released: {key}")

    def start_state_timer(self, state):
        """ Start the timer for a given state """
        self.state_start_times[state] = time.time()

    def get_state_duration(self, state):
        """ Calculate the duration spent in a given state """
        return time.time() - self.state_start_times.get(state, time.time())
    def StateActivity(self, state, mouse1, mouse2):
        if state is not None:
            duration = self.get_state_duration(state)
            self.event_logger.log_event_data(self.numcompletedtrial,state,duration)

        if state == States.Start:


            self.visit_cen=False


        #elif state == States.WaitForStart:
        #    pass

        elif state == States.CenterReward:

            self.time_to_make_decision = 0
            self.time_to_return_to_center = 0

            print(self.timestamps)
            self.center_cnt += 1
            self.visit_cen=True
            print("delivering reward in the center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time)
            mouse2.DeliverReward(Locations.Center, self.center_reward_time)



        elif state == States.TrialStarted:
            Play(Sounds.Start)
            self.time_start = time.time()

            if self.numcompletedtrial > 0:

                    self.time_to_return_to_center = time.time() - self.time_to_make_decision- self.time_start
            mouse1.NewTrial()
            mouse2.NewTrial()

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "0.03"
            self.opponent_reward = "0.03"
            self.mouse_center_reward="0.0"
            self.opponent_center_reward = "0.0"
            self.cc_cnt += 1
            mouse1.DeliverReward(Locations.Cooperate, self.reward_time)
            mouse2.DeliverReward(Locations.Cooperate, self.reward_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0"
            self.opponent_reward = "0.06"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            self.cd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.sucker_time)
            mouse2.DeliverReward(Locations.Cooperate, self.temptation_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward = "0.06"
            self.opponent_reward = "0"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            self.dc_cnt += 1
            mouse1.DeliverReward(Locations.Cooperate, self.temptation_time)
            mouse2.DeliverReward(Locations.Defect, self.sucker_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1DM2D:
            # Actions for M1DM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "0.015"
            self.opponent_reward = "0.015"
            self.mouse_center_reward = "0.0"
            self.opponent_center_reward = "0.0"
            self.dd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.punishment_time)
            mouse2.DeliverReward(Locations.Defect, self.punishment_time)
            self.time_to_make_decision = time.time() - self.time_start




        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1

            self.timestamps = {
                'Start Time': self.time_start,
                'Decision Time': self.time_to_make_decision,
                'Return Time': self.time_to_return_to_center
            }
            if self.visit_cen==True:
                self.mouse_center_reward = "0.002"
                self.opponent_center_reward = "0.002"
            else:
                self.mouse_center_reward = "0.00"
                self.opponent_center_reward = "0.00"

            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice,
                                             self.mouse_choice, self.mouse_reward,self.mouse_center_reward, self.opponent_reward,self.opponent_center_reward,
                                             self.time_start, self.time_to_make_decision, self.time_to_return_to_center)


        elif state == States.ReturnTimeOut:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Log that the trial has been aborted
            print("Trial has been aborted.")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"
            self.opponent_center_reward = "0.00"
            self.mouse_center_reward = "0.00"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Not Completed Trial", self.opponent_choice,
                                             self.mouse_choice, self.mouse_reward,self.mouse_center_reward, self.opponent_reward,self.opponent_center_reward,
                                             self.time_start, self.time_to_make_decision, self.time_to_return_to_center)
            self.visit_cen == False


        elif state == States.DecisionTimeOut:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"
            self.opponent_center_reward = "0.00"
            self.mouse_center_reward = "0.00"

            self.trial_logger.log_trial_data(self.numcompletedtrial, "Not Completed Trial", self.opponent_choice,
                                         self.mouse_choice, self.mouse_reward, self.mouse_center_reward,
                                         self.opponent_reward, self.opponent_center_reward,
                                         self.time_start, self.time_to_make_decision, self.time_to_return_to_center)


        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            self.trial_logger.finalize_logging()
            
    def get_data_file_path(self):
        # Retrieve the file path from the TrialLogger instance
        return self.trial_logger.get_csv_file_path()


    def start_streaming_exp(self, experiment_parameters, mouse1, mouse2, opponent_path):
        self.trial_logger.start_logging(experiment_parameters.get("mouse_id"), opponent_path)
        self.num_trial = experiment_parameters.get("num_trials")
        force_end_time = self.num_trial * (experiment_parameters.get("decision_time") + experiment_parameters.get("return_time"))

        self.stateManager.SetTimeOut(experiment_parameters.get("decision_time"), experiment_parameters.get("return_time"))

        currentstate = None
        state_history = []
        listener = Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        while currentstate != States.End:

            self.trialevents = 0
            """""
            if self.experimenter.check_for_start():
                # If true, trigger the trial start event
                print("Experimenter has initiated the trial.")
                self.trialevents += Events.StartTrial.value
            """
            if self.numcompletedtrial == self.num_trial:
                self.trialevents += Events.LastTrial.value

            if self.reward_manager.is_reward_delivered():
                self.trialevents += Events.RewardDelivered.value

            zone_activations = self.videoAnalyser.process_single_frame(self.timestamps)
            # print("zone activations", zone_activations)  ##just for debugging purposes

            first_opponent_choice = mouse1.getDecision(zone_activations)
            Second_opponent_choice = mouse2.getDecision(zone_activations)

            if first_opponent_choice == Locations.Center:
                self.trialevents = self.trialevents + Events.Mouse1InCenter.value
            elif first_opponent_choice == Locations.Cooperate:
                self.trialevents = self.trialevents + Events.Mouse1Cooporated.value
            elif first_opponent_choice == Locations.Defect:
                self.trialevents = self.trialevents + Events.Mouse1Defected.value

            if Second_opponent_choice == Locations.Center:
                self.trialevents = self.trialevents + Events.Mouse2InCenter.value
            elif Second_opponent_choice == Locations.Cooperate:
                self.trialevents = self.trialevents + Events.Mouse2Cooporated.value
            elif Second_opponent_choice == Locations.Defect:
                self.trialevents = self.trialevents + Events.Mouse2Defected.value
            with self.event_lock:
                if self.trialevents ==Events.ExperimentStopped.value:
                    print("Stopping experiment due to user input.")


            nextstate = self.stateManager.DetermineState(self.trialevents)

            if nextstate != currentstate:
                currentstate = nextstate
                print(f"Current State: {currentstate}")
                state_history.append(currentstate)
                self.StateActivity(currentstate, mouse1, mouse2)
