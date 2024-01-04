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
from modelling_opponent.simulated_mouse import Simulated_mouse
#from modelling_opponent.Simulated_learner import Simulated_mouse
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Reward_manager.RewardManager import RewardManager
from Data_analysis.logger import TrialLogger
from modelling_opponent.OpponentType import OpponentType
from Experiment_Launcher_code import Experimenter
import atexit

class ExperimentManager:
    def __init__(self):
        # initialize software components
        self.mouse_id="1780"
        self.videoAnalyser = Video_Analyzer(self.mouse_id)
        self.stateManager = StateManager()
        self.trial_logger = TrialLogger()
        self.stateHistories = {}
        #initialize data_analyser
        #self.data_analyzer = DataAnalyzer(self.data_path)
        # Initialize Arduino board
        self.initialize_arduino()
        #initialize reward manager
        self.reward_manager = RewardManager(self.board, [7, 8, 9, 10, 11, 12])
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
        self.trial_logger.start_logging(self.mouse_id)
        atexit.register(self.trial_logger.finalize_logging)
    def initialize_arduino(self):
        comport = "COM11"
        self.board = ArduinoDigital(comport)

    def StateActivity(self, state, mouse1simulated, mouse2simulated):
        if state == States.Start:
            Play(Sounds.Start)

            pass

        #elif state == States.WaitForStart:
        #    pass

        elif state == States.CenterReward:
            self.center_cnt += 1
            print("delivering reward in the center ")
            self.reward_manager.deliver_reward('center', 1, self.punishment_time)
            self.reward_manager.deliver_reward('center', 2, self.punishment_time)
            """""
            if not mouse1simulated:

                self.reward_manager.deliver_reward('dd', 8, self.punishment_time)
            if not mouse2simulated:
                self.reward_manager.deliver_reward('dd', 11, self.punishment_time)
            """

        elif state == States.TrialStarted:

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
            self.reward_manager.deliver_reward('cc', 1, self.reward_time)
            self.reward_manager.deliver_reward('cc', 2, self.reward_time)
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
            self.reward_manager.deliver_reward('cd', 1, self.reward_time)
            self.reward_manager.deliver_reward('cd', 2, self.punishment_time)
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

            self.reward_manager.deliver_reward('dc', 1, self.punishment_time)
            self.reward_manager.deliver_reward('dc', 2, self.reward_time)
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
            self.reward_manager.deliver_reward('dd', 1, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 2, self.punishment_time)
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
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Log that the trial has been aborted
            print("Trial has been aborted.")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"

            self.trial_logger.log_trial_data(self.numcompletedtrial, "Return Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.DecisionAbort:
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A"
            self.mouse_choice = "N/A"
            self.mouse_reward = "-"
            self.opponent_reward = "-"

            self.trial_logger.log_trial_data(self.numcompletedtrial, "Decision Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

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
            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = MouseMonitor(self.videoAnalyser, 2)
            mouse2sim = None
            self.opponent_type ="MOUSE_MOUSE"  ##for the logger
        elif opponent_type == OpponentType.MOUSE_COMPUTER:

            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent1_strategy)
            mouse2sim = mouse2
            self.opponent_type = "MOUSE_COMPUTER"  ##for the logger
        else:
            mouse1 = Simulated_mouse()
            mouse1.SetStrategy(opponent1_strategy)
            mouse1sim = mouse1
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent2_strategy)
            mouse2sim = mouse2
            self.opponent_type = "COMPUTER_COMPUTER" ##for the logger

        self.stateManager.SetTimeOuts(decision_time, return_time)

        currentstate = None
        mouse1location = None
        mouse2location = None

        state_history = []

        while currentstate != States.End:
            trialevents = 0;
            print("current state",currentstate)
            if self.numcompletedtrial not in self.stateHistories:
                self.stateHistories[self.numcompletedtrial] = []
            self.stateHistories[self.numcompletedtrial].append(currentstate)
            if self.numcompletedtrial == self.num_trial:
                trialevents += Events.LastTrial.value
            else:
                zone_activations = self.videoAnalyser.process_single_frame()


                if opponent_type == OpponentType.MOUSE_MOUSE:

                    # Retrieve locations from both queues for real mice
                    mouselocation = mouse1.getDecision(zone_activations)
                    opponent_choice = mouse2.getDecision(zone_activations)
                elif opponent_type == OpponentType.MOUSE_COMPUTER:
                    # Retrieve location for the real mouse from its queue and get the simulated mouse's location
                    mouselocation = mouse1.getDecision(zone_activations, currentstate)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Unknown, currentstate)
                else:


                    mouselocation = mouse1sim.get_mouse_location(Locations.Unknown, currentstate)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Unknown, currentstate)

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
                print(f"Current State: {nextstate}")
                state_history.append(currentstate)
                self.StateActivity(currentstate, mouse1sim, mouse2sim)

