from Sound_manager_code.SoundManager import Play, Sounds
from Video_analyser_code.VideoAnalyser import Video_Analyzer


from modelling_opponent.MouseMonitor1 import MouseMonitor
#from Video_analyser_code.VideoAnalyzerStub import Video_Analyzer
from modelling_opponent.MouseMonitor1 import Locations
#from modelling_opponent.simulated_mouse import Simulated_mouse
from modelling_opponent.Simulated_learner import Simulated_mouse
from Arduino_related_code.ArduinoDigital import ArduinoDigital
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Reward_manager.RewardManager import RewardManager
import tkinter as tk
from Data_analysis.logger import TrialLogger
from modelling_opponent.OpponentType import OpponentType
from Data_analysis.DataAnalysisScript import DataAnalyzer
from Experiment_Launcher_code.Experimenter import Experimenter
# from ArduinoDigitalSim import ArduinoDigital  ##Anushka-new class
class ExperimentManager:
    def __init__(self):
        #initialize video analyser
        self.videoAnalyser = Video_Analyzer()   ##Changed to accept nothing

        #initialize state manager
        self.stateManager = StateManager()
        self.experimenter = Experimenter(self.videoAnalyser)
        # initialize path to store data
        self.data_path = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/abcdefghi.csv'  ###change to whatever.csv
        # initialize trial logger
        self.trial_logger = TrialLogger(self.data_path)
        #initialize data_analyser
        self.data_analyzer = DataAnalyzer(self.data_path)
        # Initialize Arduino board
        self.initialize_arduino()
        #initialize reward manager
        self.reward_manager = RewardManager(self.board, [7, 8, 9, 10, 11, 12])
        #initialize experimenter
        #self.experimenter = Experimenter(self.videoAnalyser)

        def initialize_arduino(self):
            comport = "COM11"
            self.board = ArduinoDigital(comport)

        # Set default reward and punishment times
        self.reward_time = 0.2
        self.sucker_time = 0
        self.temptation_time = 0.09
        self.punishment_time = 0.004
        self.center_reward_time = 1
        self.numcompletedtrial = 0
        self.num_trial = 0
        # set variables
        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0


    def initialize_arduino(self):
        comport = "COM11"
        self.board = ArduinoDigital(comport)

    def StateActivity(self, state, mouse1simulated, mouse2simulated):
        ExperimentCompleted = False

        if state == States.Start:
            # Initialize variables, set some flags, start recording, etc.
            pass

        elif state == States.WaitForStart:
           pass


        elif state == States.CenterReward:
            self.center_var = True
            self.center_cnt += 1
            print("delivering reward in the center ")
            self.reward_manager.deliver_reward('center', 1, self.punishment_time)   ##i wanted to test the reward system without the mice so im using the simulated mice for now
            self.reward_manager.deliver_reward('center', 2, self.punishment_time)
            """""
            if not mouse1simulated:

                self.reward_manager.deliver_reward('dd', 8, self.punishment_time)
            if not mouse2simulated:
                self.reward_manager.deliver_reward('dd', 11, self.punishment_time)
            """
        elif state == States.TrialStarted:
            Play(Sounds.Start)

            if mouse1simulated:
                mouse1simulated.NewTrial()
            if mouse2simulated:
                mouse2simulated.NewTrial()

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "12"
            self.opponent_reward = "12"
            self.cc_cnt += 1
            #self.reward_manager.deliver_reward('cc', 1, self.reward_time)
            #self.reward_manager.deliver_reward('cc', 2, self.reward_time)
            """""
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cc', 1, self.reward_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cc', 2, self.reward_time)
            """
        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0"
            self.opponent_reward = "15"
            self.cd_cnt += 1
            #self.reward_manager.deliver_reward('cd', 1, self.reward_time)
            #self.reward_manager.deliver_reward('cd', 2, self.punishment_time)
            """""
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cd', 1, self.reward_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cd', 2, self.punishment_time)
            """
        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward = "15"
            self.opponent_reward = "0"
            self.dc_cnt += 1

            #self.reward_manager.deliver_reward('dc', 1, self.punishment_time)
            #self.reward_manager.deliver_reward('dc', 2, self.reward_time)
            """""
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dc', 1, self.punishment_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dc', 2, self.reward_time)
            """
        elif state == States.M1DM2D:
            # Actions for M1DDM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "15"
            self.opponent_reward = "15"
            self.dd_cnt += 1
            #self.reward_manager.deliver_reward('dd', 1, self.punishment_time)
            #self.reward_manager.deliver_reward('dd', 2, self.punishment_time)
            """""
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dd', 1, self.punishment_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dd', 2, self.punishment_time)
            """
        elif state == States.WaitForReturn:
            Play(Sounds.Abort)


        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice, self.mouse_choice, self.mouse_reward, self.opponent_reward)

        elif state == States.TrialAbort:
            # Log that the trial has been aborted
            print("Trial has been aborted.")  # Or use a logging mechanism if available
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Return Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.DecisionAbort:
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Decision Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            self.trial_logger.finalize_logging()
            analysis_results = self.data_analyzer.analyze_data()

            print(analysis_results)
            ExperimentCompleted = True

        return ExperimentCompleted

    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent1_strategy,
                            opponent2_strategy):
        # OPEN CSV TO LOG DETAILS
        self.num_trial = num_trial
        print("opponent ", opponent_type)
        print("opponent strategy ", opponent1_strategy)

        if opponent_type == OpponentType.MOUSE_MOUSE:
            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = MouseMonitor(self.videoAnalyser, 2)
            mouse2sim = None
        elif opponent_type == OpponentType.MOUSE_COMPUTER:

            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent1_strategy)
            mouse2sim = mouse2
        else:

            mouse1 = Simulated_mouse()
            mouse1.SetStrategy(opponent1_strategy)
            mouse1sim = mouse1
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent2_strategy)
            mouse2sim = mouse2
        self.stateManager.SetTimeOuts(duration, time_decision)

        currentstate = States.WaitForStart
        mouse1location = None
        mouse2location = None

        state_history = []
        while currentstate != States.End:
            print(f"Current State: {currentstate}")

            trialevents = 0;

            if currentstate==States.WaitForStart and self.experimenter.check_for_start():
                # If true, trigger the trial start event

                    print("Experimenter has initiated the trial.")
                    trialevents += Events.StartTrial.value

            elif self.numcompletedtrial == self.num_trial - 1:

                trialevents += Events.LastTrial.value
                # print("TRIAL COMPLETE EVENTS", trialevents)

            else:
                zone_activations = self.videoAnalyser.process_single_frame()
                #print("zone activations", zone_activations)  ##just for debugging purposes

                if opponent_type == OpponentType.MOUSE_MOUSE:

                    # Retrieve locations from both queues for real mice
                    mouselocation = mouse1.get_mouse_location(zone_activations, currentstate)
                    opponent_choice = mouse2.get_mouse_location(zone_activations, currentstate)
                elif opponent_type == OpponentType.MOUSE_COMPUTER:
                    # Retrieve location for the real mouse from its queue and get the simulated mouse's location
                    mouselocation = mouse1.get_mouse_location(zone_activations,currentstate)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Center, currentstate)
                else:
                    # Retrieve locations from simulated mice methods

                    mouselocation = mouse1sim.get_mouse_location(Locations.Center, currentstate)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Center, currentstate)
                    #print("mouselocation", mouselocation) ##just for debugging purposes
                    #print("opponent_choice", opponent_choice) ##just for debugging purposes
                if mouselocation == Locations.Center:
                    trialevents = trialevents + Events.Mouse1InCenter.value
                elif mouselocation == Locations.Cooperate:
                    trialevents = trialevents + Events.Mouse1Cooporated.value
                elif mouselocation == Locations.Defect:
                    trialevents = trialevents + Events.Mouse1Defected.value

                if opponent_choice == Locations.Center:
                    trialevents = trialevents + Events.Mouse2InCenter.value
                elif opponent_choice == Locations.Cooperate:
                    trialevents = trialevents + Events.Mouse2Cooporated.value
                elif opponent_choice == Locations.Defect:
                    trialevents = trialevents + Events.Mouse2Defected.value

            nextstate = self.stateManager.DetermineState(trialevents)

            # print(f"next State: {nextstate}")
            if nextstate != currentstate:
                currentstate = nextstate
                print(f"Current State: {nextstate}")  # Micky: A slight change of order and text to improve readability
                self.StateActivity(currentstate, mouse1sim, mouse2sim)

