# The first group of import statements control the simulated vs real HW environments

from Video_analyser_code.VideoAnalyser import Video_Analyzer
#from Video_analyser_code.VideoAnalyzerStub import Video_Analyzer
#from Video_analyser_code.VideoAnalyzerSim import Video_Analyzer

from Arduino_related_code.ArduinoDigital import ArduinoDigital
#from Arduino_related_code.ArduinoDigitalSim import ArduinoDigital

# The following are configuration independent imports
from Sound_manager_code.SoundManager import Play, Sounds
from modelling_opponent.MouseMonitor import MouseMonitor
from modelling_opponent.MouseMonitor import Locations
from modelling_opponent.FixedStrategyPrisoner import FixedStrategyPrisoner
#from modelling_opponent.Simulated_learner import Simulated_mouse
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Reward_manager.RewardManager import RewardManager
from Data_analysis.logger import TrialLogger
from modelling_opponent.OpponentType import OpponentType
from Experiment_Launcher_code import Experimenter
from Reward_manager.RewardManager import RewardManager
import time


class ExperimentManager:
    def __init__(self, comport):
        # initialize software components
        self.reward_manager = RewardManager(comport)

        self.mouse_id="2000"
        self.videoAnalyser = Video_Analyzer(self.mouse_id)
        self.stateManager = StateManager()
        self.trial_logger = TrialLogger()

        #initialize data_analyser
        #self.data_analyzer = DataAnalyzer(self.data_path)

        #initialize reward manager

        self.opponent_type = ""  ##for the logger

        # Set default reward and punishment times
        self.reward_time = 0.2
        self.sucker_time = 0
        self.temptation_time = 0.09
        self.punishment_time = 0.004
        self.center_reward_time = 0.05

        # initialize experiment control variables
        self.numcompletedtrial = 0
        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0

        self.time_start = None
        self.time_to_make_decision = None
        self.time_to_return_to_center = None
        self.timestamps={}##for the video writer

    def StateActivity(self, state, mouse1, mouse2):
        if state == States.Start:
            self.time_start = time.time()
            self.time_to_make_decision =0
            self.time_to_return_to_center = 0
            self.timestamps = {
                'Start Time': self.time_start,
                'Decision Time': self.time_to_make_decision,
                'Return Time': self.time_to_return_to_center
            }


        #elif state == States.WaitForStart:
        #    pass

        elif state == States.CenterReward:
            self.time_start = time.time()
            self.time_to_make_decision = 0
            self.time_to_return_to_center = 0

            print(self.timestamps)
            self.center_cnt += 1
            print("delivering reward in the center ")
            mouse1.DeliverReward(Locations.Center, self.center_reward_time)
            mouse2.DeliverReward(Locations.Center, self.center_reward_time)


        elif state == States.TrialStarted:
            Play(Sounds.Start)
            mouse1.NewTrial()
            mouse2.NewTrial()

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "12"
            self.opponent_reward = "12"
            self.cc_cnt += 1
            mouse1.DeliverReward(Locations.Cooperate, self.reward_time)
            mouse2.DeliverReward(Locations.Cooperate, self.reward_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0"
            self.opponent_reward = "15"
            self.cd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.sucker_time)
            mouse2.DeliverReward(Locations.Cooperate, self.temptation_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward = "15"
            self.opponent_reward = "0"
            self.dc_cnt += 1
            mouse1.DeliverReward(Locations.Cooperate, self.temptation_time)
            mouse2.DeliverReward(Locations.Defect, self.sucker_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.M1DM2D:
            # Actions for M1DM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "15"
            self.opponent_reward = "15"
            self.dd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.punishment_time)
            mouse2.DeliverReward(Locations.Defect, self.punishment_time)
            self.time_to_make_decision = time.time() - self.time_start

        elif state == States.WaitForReturn:
            pass


        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            if self.numcompletedtrial > 0:

                    self.time_to_return_to_center = time.time() - self.time_to_make_decision- self.time_start
            self.timestamps = {
                'Start Time': self.time_start,
                'Decision Time': self.time_to_make_decision,
                'Return Time': self.time_to_return_to_center
            }


            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice,
                                             self.mouse_choice, self.mouse_reward, self.opponent_reward,
                                             self.time_start, self.time_to_make_decision, self.time_to_return_to_center)


        elif state == States.TrialAbort:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Log that the trial has been aborted
            print("Trial has been aborted.")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"

            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice,
                                             self.mouse_choice, self.mouse_reward, self.opponent_reward,
                                             self.time_start, self.time_to_make_decision, self.time_to_return_to_center)


        elif state == States.DecisionAbort:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"

            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice,
                                             self.mouse_choice, self.mouse_reward, self.opponent_reward,
                                             self.time_start, self.time_to_make_decision, self.time_to_return_to_center)


        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            self.trial_logger.finalize_logging()
            analysis_results = self.data_analyzer.analyze_data()
            print(analysis_results)

    def start_streaming_exp(self, experiment_name, num_trial, decision_time, return_time, opponent_type, opponent1_strategy, opponent2_strategy):
        self.trial_logger.start_logging(experiment_name)
        self.num_trial = num_trial
        print("opponent ", opponent_type)
        print("opponent strategy ", opponent1_strategy)

        if opponent_type == OpponentType.MOUSE_MOUSE:
            mouse1 = MouseMonitor(1, self.videoAnalyser, self.reward_manager)
            mouse2 = MouseMonitor(2, self.videoAnalyser, self.reward_manager)
        elif opponent_type == OpponentType.MOUSE_COMPUTER:
            mouse1 = MouseMonitor(1, self.videoAnalyser, self.reward_manager)
            mouse2 = FixedStrategyPrisoner(opponent1_strategy, probability=0.8)
        else:
            mouse1 = FixedStrategyPrisoner(opponent1_strategy, probability=0.8)
            mouse2 = FixedStrategyPrisoner(opponent2_strategy, probability=0.8)

        self.stateManager.SetTimeOut(decision_time, return_time)

        currentstate = None
        state_history = []

        while currentstate != States.End:
            trialevents = 0
            """""
            if self.experimenter.check_for_start():
                # If true, trigger the trial start event
                print("Experimenter has initiated the trial.")
                trialevents += Events.StartTrial.value
            """
            if self.numcompletedtrial == self.num_trial:
                trialevents += Events.LastTrial.value

            if self.reward_manager.is_reward_delivered():
                trialevents += Events.RewardDelivered.value

            zone_activations = self.videoAnalyser.process_single_frame(self.timestamps)
            #print("zone activations", zone_activations)  ##just for debugging purposes

            first_opponent_choice = mouse1.getDecision(zone_activations)
            Second_opponent_choice = mouse2.getDecision(zone_activations)

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

            if nextstate != currentstate:
                currentstate = nextstate
                print(f"Current State: {currentstate}")
                state_history.append(currentstate)
                self.StateActivity(currentstate, mouse1, mouse2)

