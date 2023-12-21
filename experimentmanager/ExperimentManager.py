import threading
from opponent.MouseMonitor import MouseMonitor
from videoanalyser.VideoAnalyzerStub import VideoAnalyzerStub
from opponent.MouseMonitor import Locations
#from simulated_mouse import Simulated_mouse
from opponent.SimulatedLearner import Simulated_mouse
#from ArduinoDigital import ArduinoDigital
from statemanager.StateManager import StateManager
from statemanager.StateManager import States
from statemanager.StateManager import Events
from RewardManager import RewardManager
import tkinter as tk
from logger import TrialLogger
from arduino.ArduinoDigitalSim import ArduinoDigital
from StartDelayHandler import StartDelayHandler
from queue import Queue
class ExperimentManager:
    def __init__(self,opp):
        # Initialize other components here
        #self.videoAnalyser = VideoAnalyzer()

        self.mouse_location_queue = Queue()
        self.num_trial=0
        self.opponent_type=opp
        self.root = tk.Tk()
        self.root.withdraw()
        #self.videoAnalyser = VideoAnalyzerStub(self.root, self.mouse_location_queue)##puts data into queue
        self.trial_logger = TrialLogger("C:/Users/anush/Downloads/PrisonerDilemmaPy_(4)")
        #self.mouse1 = MouseMonitor(self.mouse_location_queue, mouse_id=1)#gets data from queue
        #self.mouse2 = MouseMonitor(self.mouse_location_queue, mouse_id=2)
        if opp == "mouse_mouse":
            # Initialize for real mouse vs. real mouse
            self.mouse_location_queue_1 = Queue()
            self.mouse_location_queue_2 = Queue()

            self.top_level_1 = tk.Toplevel(self.root)
            self.video_analyzer_1 = VideoAnalyzerStub(self.top_level_1, self.mouse_location_queue_1)
            self.mouse1 = MouseMonitor(self.mouse_location_queue_1, mouse_id=1)

            self.top_level_2 = tk.Toplevel(self.root)
            self.video_analyzer_2 = VideoAnalyzerStub(self.top_level_2, self.mouse_location_queue_2)
            self.mouse2 = MouseMonitor(self.mouse_location_queue_2, mouse_id=2)

        elif opp == "mouse_computer":
            # Initialize for real mouse vs. simulated mouse
            self.mouse_location_queue_1 = Queue()
            self.top_level_1 = tk.Toplevel(self.root)
            self.video_analyzer_1 = VideoAnalyzerStub(self.top_level_1, self.mouse_location_queue_1)
            self.mouse1 = MouseMonitor(self.mouse_location_queue_1, mouse_id=1)

            self.opponent1 = Simulated_mouse(self.mouse_location_queue_1, mouse_id=2)

        else:  # "computer and computer"
            # Initialize for simulated mouse vs. simulated mouse
            self.opponent1 = Simulated_mouse(Queue(), mouse_id=1)
            self.opponent2 = Simulated_mouse(Queue(), mouse_id=2)
        """""
        self.root = tk.Tk()
        self.root.withdraw()
        self.mouse_location_queue_1 = Queue()
        self.mouse_location_queue_2 = Queue()

        # Main window for the first mouse
        self.top_level_1 = tk.Toplevel(self.root)
        self.video_analyzer_1 = VideoAnalyzerStub(self.top_level_1, self.mouse_location_queue_1)
        self.mouse1 = MouseMonitor(self.mouse_location_queue_1, mouse_id=1)

        # Separate window for the second mouse
        self.top_level_2 = tk.Toplevel(self.root)
        self.video_analyzer_2 = VideoAnalyzerStub(self.top_level_2, self.mouse_location_queue_2)
        self.mouse2 = MouseMonitor(self.mouse_location_queue_2, mouse_id=2)
        #self.mouse1 = MouseMonitor(self.videoAnalyser, 1)
        #self.mouse2 = MouseMonitor(self.videoAnalyser, 2)
        self.opponent1 = Simulated_mouse(self.mouse_location_queue_2,mouse_id=1)
        self.opponent2 = Simulated_mouse(self.mouse_location_queue_1,mouse_id=2)
        """""

        self.numcompletedtrial=0
        self.stateManager = StateManager()

        # Initialize Arduino board
        self.initialize_arduino()

        # Set default reward and punishment times
        self.reward_time = 0.02
        self.sucker_time = 0
        self.temptation_time = 0.009
        self.punishment_time = 0.004
        self.center_reward_time = 0.1
        self.numcompletedtrial=0
        # Initialize CSV file and video capture
        #self.initialize_csv_logging()
        #self.initialize_video_capture()


        ### VARIABLES FOR LOG FILE INITIALLY INITIALIZED TO FALSE
        self.data_file_loc = 'path_to_csv_file.csv'
        self.cc_var = False
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
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        ###evaluation metrics
        self.agent1_total_reward = 0
        self.agent2_total_reward = 0
        self.agent1_steps = 0
        self.agent2_steps = 0
    def initialize_arduino(self):
        comport="5"
        self.board = ArduinoDigital(comport)
        # Set all pins to low
        for pin in [7, 8, 9, 10, 11, 12]:
            self.board.DigitalLow(pin)
    def start_gui(self):
        self.root.mainloop()
    def start_gui_in_thread(self):
        # Start GUI in a new thread
        gui_thread = threading.Thread(target=self.start_gui)
        gui_thread.start()

    def on_close(self):
        # Destroy the Toplevel windows
        self.top_level_1.destroy()
        self.top_level_2.destroy()

        # Finally, destroy the main window
        self.root.destroy()

    def on_delay_complete(self):
        # This function will be called after the delay
        # Continue with the experiment setup or start the next state
        print("Start state delay complete.")
    def start_experiment_in_thread(self, num_trial, duration, time_decision, opponent_type, opponent1_strategy,opponent2_strategy):
        # Start streaming experiment in a new thread
        experiment_thread = threading.Thread(target=self.start_streaming_exp, args=(num_trial, duration, time_decision, opponent_type, opponent1_strategy,opponent2_strategy))
        experiment_thread.start()
    def StateActivity(self, state):
        self.agent1_steps += 1
        self.agent2_steps += 1

        if state == States.Start:
            # Increment the trial number counter in the TrialControl state

            time_buffer_duration = 5  # Time buffer in seconds
            delay_handler = StartDelayHandler(time_buffer_duration, self.on_delay_complete)
            delay_handler.start_delay()
            self.numcompletedtrial += 1


            trial_number = self.numcompletedtrial  # Adjust as needed
            trial_validity = (
                    (self.cc_var and self.center_var) or
                    (self.cd_var and self.center_var) or
                    (self.dc_var and self.center_var) or
                    (self.dd_var and self.center_var)
            )
            if self.cc_var:
                mouse_choice = "C"
                opponent_choice = "C"
                mouse_reward = "12ml"
                opponent_reward = "12ml"
            elif self.cd_var:
                mouse_choice = "C"
                opponent_choice = "D"
                mouse_reward = "0ml"
                opponent_reward = "15ml"
            elif self.dc_var:
                mouse_choice = "D"
                opponent_choice = "C"
                mouse_reward = "15ml"
                opponent_reward = "0ml"
            elif self.dd_var:
                mouse_choice = "D"
                opponent_choice = "D"
                mouse_reward = "15ml"
                opponent_reward = "15ml"
            else:
                # Handle the case when none of the conditions are met
                mouse_choice = "N/A"
                opponent_choice = "N/A"
                mouse_reward = "-"
                opponent_reward = "-"
            self.trial_logger.log_trial_data(trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,
                                             opponent_reward)





        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            print("in MICM2C")
            self.cc_var = True
            self.cc_cnt += 1
            self.reward_manager.deliver_reward('cc', 12, self.reward_time)
            self.reward_manager.deliver_reward('cc', 7, self.reward_time)

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.cd_var = True
            self.cd_cnt += 1
            self.reward_manager.deliver_reward('cd', 12, self.reward_time)
            self.reward_manager.deliver_reward('cd', 9, self.punishment_time)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.dc_var = True
            self.dc_cnt += 1
            self.reward_manager.deliver_reward('dc', 10, self.punishment_time)
            self.reward_manager.deliver_reward('dc', 7, self.reward_time)

        elif state == States.M1DM2D:
            # Actions for M1DDM2D state
            self.dd_var = True
            self.dd_cnt += 1
            self.reward_manager.deliver_reward('dd', 10, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 9, self.punishment_time)

        elif state == States.WaitForReturn:
            # Handle WaitForReturn state
            pass  # Placeholder for WaitForReturn logic

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)






        elif state == States.TrialAbort:
         print("IN TRIAL ABORT")
         pass

        elif state == States.DecisionAbort:
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            pass  # Placeholder for DecisionAbort logic

        elif state == States.CenterReward:
            self.center_var = True
            self.center_cnt += 1
            self.reward_manager.deliver_reward('dd', 8, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 11, self.punishment_time)



        elif state == States.TrialAbort:
            # Log that the trial has been aborted
            print("Trial has been aborted.")  # Or use a logging mechanism if available
            trial_validity = 0
            # Update the logger with the aborted trial information
            self.trial_logger.log_trial_data(
                trial_number=self.numcompletedtrial,
                trial_validity=trial_validity,
                opponent_choice="N/A",
                mouse_choice="N/A",
                mouse_reward="-",
                opponent_reward="-"
            )



        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            self.evaluate_agent_performance()
            print("END OF EXPERIMENT")

    def evaluate_agent_performance(self):
        # Calculate collective reward
        collective_reward = self.agent1_total_reward + self.agent2_total_reward

        # Print the metrics
        print(f"Agent 1 Total Reward: {self.agent1_total_reward}, Steps: {self.agent1_steps}")
        print(f"Agent 2 Total Reward: {self.agent2_total_reward}, Steps: {self.agent2_steps}")
        print(f"Collective Reward: {collective_reward}")

    def map_location_to_enum(self,array_input):
        if array_input == [0, 0, 0]:
            return Locations.Unknown.value
        elif array_input == [1, 0, 0]:
            return Locations.Cooperate.value
        elif array_input == [0, 1, 0]:
            return Locations.Center.value
        elif array_input == [0, 0, 1]:
            return Locations.Defect.value
        else:
            return Locations.Unknown.value

    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent1_strategy,opponent2_strategy):

            self.num_trial=num_trial
            self.stateManager.SetTimeOuts(duration, time_decision)



            currentstate = States.Start

            mouselocation = None
            state_history = []
            self.StateActivity(currentstate)
            while currentstate != States.End:
                print("Number completed trial",self.numcompletedtrial)

                if self.numcompletedtrial == self.num_trial-1 :

                    trialevents |= Events.LastTrial.value
                    print("TRIAL COMPLETE EVENTS",trialevents)
                else:
                    #print(f"Current State: {currentstate}")
                    state_history.append(currentstate)
                    trialevents = 0  # Initialize trialevents as 0 (no events)

                    # Get mouse locations
                    if opponent_type == "mouse_mouse":
                        # Retrieve locations from both queues for real mice
                        mouselocation = self.mouse_location_queue_1.get()
                        opponent_choice = self.mouse_location_queue_2.get()
                    elif opponent_type == "mouse_computer":
                        # Retrieve location for the real mouse from its queue and get the simulated mouse's location
                        mouselocation = self.mouse_location_queue_1.get()
                        self.opponent1.SetStrategy(opponent1_strategy)
                        opponent_choice = self.opponent1.GetMouseLocation([0,1,0],currentstate)  # Assuming the method can be called without actual location

                    else:
                        # Retrieve locations from simulated mice methods
                        self.opponent1.SetStrategy(opponent1_strategy)
                        mouselocation = self.opponent1.GetMouseLocation([0,1,0],currentstate,1)
                        self.opponent2.SetStrategy(opponent2_strategy)
                        opponent_choice = self.opponent2.GetMouseLocation([0,1,0],currentstate,2)

                    # Convert locations to enum values
                    mouse1_location_enum = self.map_location_to_enum(mouselocation)
                    mouse2_location_enum = self.map_location_to_enum(opponent_choice)
                    print("mouse 1 location ", mouselocation)
                    print("mouse 2 location ", opponent_choice)

                    reward_for_agent1=self.opponent1.reward
                    reward_for_agent2=self.opponent2.reward
                    self.agent1_total_reward += reward_for_agent1
                    self.agent2_total_reward += reward_for_agent2

                    #print("mouse 1 location ", mouse1_location_enum)
                    #print("mouse 2 location ", mouse2_location_enum)




                    # Determine events based on location enums using bitwise OR
                    if mouse1_location_enum == Locations.Cooperate.value:
                        trialevents |= Events.Mouse1Cooporated.value
                    elif mouse1_location_enum == Locations.Center.value:
                        trialevents |= Events.Mouse1InCenter.value
                    elif mouse1_location_enum == Locations.Defect.value:
                        trialevents |= Events.Mouse1Defected.value

                    if mouse2_location_enum == Locations.Cooperate.value:
                        trialevents |= Events.Mouse2Cooporated.value
                    elif mouse2_location_enum == Locations.Center.value:
                        trialevents |= Events.Mouse2InCenter.value
                    elif mouse2_location_enum == Locations.Defect.value:
                        trialevents |= Events.Mouse2Defected.value

                    # Check if the current trial is the last one

                print("trial events", trialevents)
                nextstate = self.stateManager.DetermineState(trialevents)

                if nextstate != currentstate:
                    currentstate = nextstate
                    self.StateActivity(currentstate)
                if currentstate == States.End:
                    break
