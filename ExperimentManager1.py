# Micky: I suggest to return to the original file name. the '1' suffix is confusing

from VideoAnalyzerSim import VideoAnalyzer
#from VideoAnalyser1 import Video_Analyzer
# from VideoAnalyzer import Video_Analyzer
# from VideoAnalyzerStub import Video_Analyzer

#from ArduinoDigital import ArduinoDigital
from ArduinoDigitalSim import ArduinoDigital

from MouseMonitor1 import MouseMonitor
from MouseMonitor1 import Locations
from SoundManager import *
from simulated_mouse import Simulated_mouse
from StateManager import StateManager
from StateManager import States
from StateManager import Events
from RewardManager import RewardManager
from logger import TrialLogger
from OpponentType import OpponentType


class ExperimentManager:
    def __init__(self):
        # Initialize other components here
        #self.root = tk.Tk()  # Create a new Tkinter root window if not provided   #Micky: The video Analyzer stub should create its own TK root
        # self.videoAnalyser = Video_Analyzer(self.root)
        #with Vimba.get_instance() as vimba:
            # Create Video_Analyzer instance with the active Vimba instance
            #self.videoAnalyser = Video_Analyzer(vimba)                             #Micky: The video analyzer should create its own vimb instance

        self.videoAnalyser = VideoAnalyzer()         # Micky: The real and sim classes should be defined to have identical _init__() function
                                                     #        this way changing the import staemnt will be enough to swhich bwteen real
                                                     #        and sim HW
        
        self.numcompletedtrial = 0
        self.num_trial = 0

        self.stateManager = StateManager()
        self.trial_logger = TrialLogger              # Micky: You are not passing the logfile name. Is that correct?
        # Initialize Arduino board
        self.initialize_arduino()

        # Set default reward and punishment times
        self.reward_time = 0.2
        self.sucker_time = 0
        self.temptation_time = 0.09
        self.punishment_time = 0.004
        self.center_reward_time = 1

        # Initialize CSV file and video capture       # Micky: I think it is time to delete these lines. You moved them to the relevant classes
        # self.initialize_csv_logging()
        # self.initialize_video_capture()

        ##
        ### VARIABLES FOR LOG FILE INITIALLY INITIALIZED TO FALSE
        self.data_file_loc = 'path_to_csv_file.csv'   # Micky: Use relative file name. it will make the SW more portable
        self.cc_var = False                           # Micky: It seems that you are not doinf anything with these flags. Do you really need them?
        self.cd_var = False
        self.dc_var = False
        self.dd_var = False
        self.center_var = False
        self.no_trial_var = False

        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0

        self.reward_manager = RewardManager(self.board, [7, 8, 9, 10, 11, 12])

        # self.sound_manager = SoundManager()              # Micky: According to theory, if you need only one instance of a class you
                                                           #        should define it as a static class. it runs more efficently.
                                                           #        Python has the module constarct which you can use. especially if there
                                                           #        is no class data to be stored.
                                                           #        As an example, I changed the soundManager to be a module.
                                                           #        Also, every module/class should handle its own specific data. defining
                                                           #        it (like the sound file names) in the upper level manager defeats the purpose
                                                           #        of hiding the specifics of a module,  internally to the module.
                                                           #        Take a look at how I did it.
        #self.sound_manager.load_sound('beep',
        #                              'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/sounds/beep.wav')

    def initialize_arduino(self):
        comport = "COM11"
        self.board = ArduinoDigital(comport)
        # Set all pins to low
        for pin in [7, 8, 9, 10, 11, 12]:           # Micky: This is probably what opens your vales. I think it should be changes to high
            self.board.DigitalLow(pin)              #        Also, there is no real need to initialze the vales here. You do not even want
                                                    #        to know the list of valves here. Keep the knowldege hidden in the relevant clsses.
                                                    #        it will make your code more modular and maintainable, and less prone to erros.
                                                    #        The rewardManager Class should be the only one that has the knowldge of digital channels
                                                    #        and the valveControl class should take care of initializing the valves - and it does.

                                                    #        Micky: The mouseNsimulated flags are a bad solution (I did it I know :-))
                                                    #               but Why are ignoring them in teh code? You are delivering rewards to
                                                    #               a simulated mouse. Let's discuss.
                                                    #               I will show you a better way next round.

    def StateActivity(self, state, mouse1simulated, mouse2simulated):
        ExperimentCompleted = False

        if state == States.Start:
            # Initialize variables, set some flags, start recording, etc.
            pass

        elif state == States.CenterReward:
            self.center_var = True
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
            #self.sound_manager.play_sound('beep')
            Play(Sounds.Start)
            if mouse1simulated:
                mouse1simulated.NewTrial()
            if mouse2simulated:
                mouse2simulated.NewTrial()

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "12ml"
            self.opponent_reward = "12ml"
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
            self.mouse_reward = "0ml"
            self.opponent_reward = "15ml"
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
            self.mouse_reward = "15ml"
            self.opponent_reward = "0ml"
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
            self.mouse_reward = "15ml"
            self.opponent_reward = "15ml"
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
            #self.sound_manager.play_sound('beep')            # Micky: Do we need a beep hear?
            Play(Sounds.Start)

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            # self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice, self.mouse_choice, self.mouse_reward, self.opponent_reward)
                                                        # Micky: Why are the logger writes, commented out? There is no need to.
                                                        #        If you really wanted to not log,  change it in one plcae in the logger class. Not
                                                        #        in so many places here. I assume you did it becuase you do not have the logging directory
                                                        #        on one of your computers. Use relative (rather then absolute) files names. See example in
                                                        #        in the SoundManager Class
        elif state == States.TrialAbort:
            # Log that the trial has been aborted
            print("Trial has been aborted.")  # Or use a logging mechanism if available
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            # self.trial_logger.log_trial_data(self.numcompletedtrial, "Return Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.DecisionAbort:
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            # self.trial_logger.log_trial_data(self.numcompletedtrial, "Decision Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
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
        self.stateManager.SetTimeOut(duration, time_decision)

        currentstate = None
        mouse1location = None
        mouse2location = None

        state_history = []
        while currentstate != States.End:
            # print(f"Current State: {currentstate}")
            state_history.append(currentstate)         # Micky: please rememebr that your main loop is running as fast as your computer can handle.
                                                       #        This means that your state_history is infinitly large - hense useless. If you need
                                                       #        a state history, store only the state changes.
            trialevents = 0;
            if self.numcompletedtrial == self.num_trial - 1:

                trialevents += Events.LastTrial.value
                # print("TRIAL COMPLETE EVENTS", trialevents)

            else:
                zone_activations = self.videoAnalyser.process_single_frame()
                #print("zone activations", zone_activations)    # Micky: This prints every loop cycle. way to fast to be on any use. it floods the
                                                                #         the consol window and makes it impossible to see the important data. 

                if opponent_type == OpponentType.MOUSE_MOUSE:   # Micky: This can be improved. There should be no API difference between the
                                                                # real and the simulated mice
                    # Retrieve locations from both queues for real mice
                    mouselocation = mouse1.get_mouse_location(zone_activations)
                    opponent_choice = mouse2.get_mouse_location(zone_activations)
                elif opponent_type == OpponentType.MOUSE_COMPUTER:
                    # Retrieve location for the real mouse from its queue and get the simulated mouse's location
                    mouselocation = mouse1.get_mouse_location(zone_activations)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Unknown,
                                                                   currentstate)  # Assuming the method can be called without actual location

                else:
                    # Retrieve locations from simulated mice methods

                    mouselocation = mouse1sim.get_mouse_location(Locations.Unknown, currentstate)

                    opponent_choice = mouse2sim.get_mouse_location(Locations.Unknown, currentstate)
                    #print("mouselocation", mouselocation)                        # Micky: do not print every cycle of the main loop.
                    #print("opponent_choice", opponent_choice)
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
                print(f"Current State: {nextstate}")           # Micky: A slight change of order and text to improve readability
                self.StateActivity(currentstate, mouse1sim, mouse2sim)

            if currentstate == States.End:               # Micky: No need to break. Your while loop is using the same condition.
                break