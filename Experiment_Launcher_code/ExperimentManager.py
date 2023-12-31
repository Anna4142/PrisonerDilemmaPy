from Sound_manager_code.SoundManager import Play, Sounds
from modelling_opponent.MouseMonitor import Locations
from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events
from Data_analysis.logger import TrialLogger
from Experiment_Launcher_code import Experimenter


class ExperimentManager:
    def __init__(self, video_analyzer, reward_manager):
        # initialize software components
        self.reward_manager = reward_manager
        self.videoAnalyser = video_analyzer
        self.stateManager = StateManager()
        self.trial_logger = TrialLogger()
        #initialize data_analyser
        #self.data_analyzer = DataAnalyzer(self.data_path)
        #initialize experimenter
        #self.experimenter = Experimenter(self.videoAnalyser)

        # Set default reward and punishment times
        self.reward_time = 0.2
        self.sucker_time = 0
        self.temptation_time = 0.09
        self.punishment_time = 0.004
        self.center_reward_time = 1

        # initialize experiment control variables
        self.numcompletedtrial = 0
        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0

    def StateActivity(self, state, mouse1, mouse2):
        if state == States.Start:
            pass

        #elif state == States.WaitForStart:
        #    pass

        elif state == States.CenterReward:
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

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0"
            self.opponent_reward = "15"
            self.cd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.sucker_time)
            mouse2.DeliverReward(Locations.Cooperate, self.temptation_time)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward = "15"
            self.opponent_reward = "0"
            self.dc_cnt += 1
            mouse1.DeliverReward(Locations.Cooperate, self.temptation_time)
            mouse2.DeliverReward(Locations.Defect, self.sucker_time)

        elif state == States.M1DM2D:
            # Actions for M1DM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "15"
            self.opponent_reward = "15"
            self.dd_cnt += 1
            mouse1.DeliverReward(Locations.Defect, self.punishment_time)
            mouse2.DeliverReward(Locations.Defect, self.punishment_time)

        elif state == States.WaitForReturn:
            pass

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice, self.mouse_choice, self.mouse_reward, self.opponent_reward)

        elif state == States.TrialAbort:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
            # Log that the trial has been aborted
            print("Trial has been aborted.")
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Return Abort", self.opponent_choice, self.mouse_choice,self.mouse_reward, self.opponent_reward)

        elif state == States.DecisionAbort:
            Play(Sounds.Abort)
            # Increment the trial number counter
            #self.numcompletedtrial += 1
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
            #analysis_results = self.data_analyzer.analyze_data()
            #print(analysis_results)

    def start_streaming_exp(self, experiment_parameters, mouse1, mouse2):
        self.trial_logger.start_logging(experiment_parameters.get("experiment_name"))
        self.num_trial = experiment_parameters.get("num_trials")

        self.stateManager.SetTimeOut(experiment_parameters.get("decision_time"), experiment_parameters.get("return_time"))

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

            zone_activations = self.videoAnalyser.process_single_frame()
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

