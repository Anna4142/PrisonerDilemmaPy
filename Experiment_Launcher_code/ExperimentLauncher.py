# use video analyzer import to select simulated of read mice
from Video_analyser_code.VideoAnalyser import Video_Analyzer
#from Video_analyser_code.VideoAnalyzerStub import Video_Analyzer
#from Video_analyser_code.VideoAnalyzerSim import Video_Analyzer

from modelling_opponent.MouseMonitor import MouseMonitor
from modelling_opponent.FixedStrategyPrisoner import FixedStrategyPrisoner
from modelling_opponent.Simulated_learner import Simulated_mouse
from Reward_manager.RewardManager import RewardManager
from Experiment_Launcher_code.ExperimentManager import ExperimentManager
from Experiment_Launcher_code.experimentgui import ExperimentGUI, OpponentType

def main():
    # Create an instance of the ExperimentGUI class
    experiment_gui = ExperimentGUI()
    experiment_gui.setup_gui()

    # After the GUI is closed, get the settings using the appropriate methods
    if experiment_gui.experiment_started():
        comport_name = experiment_gui.get_com_port()
        experiment_parameters = experiment_gui.get_experiment_parameters()
        opponent_configuration = experiment_gui.get_opponent_configuration()

        # Instantiate software components
        video_analyzer = Video_Analyzer("1780")
        reward_manager = RewardManager(comport_name)

        if opponent_configuration.get("opponent1_type") == OpponentType.MOUSE:
            first_opponent = MouseMonitor(1, video_analyzer, reward_manager)
        elif opponent_configuration.get("opponent1_type") == OpponentType.FIXED_STRATEGY:
            first_opponent = FixedStrategyPrisoner(opponent_configuration.get("opponent1_strategy"), opponent_configuration.get("opponent1_probability"))
        else:
            first_opponent = Simulated_mouse()

        if opponent_configuration.get("opponent2_type") == OpponentType.MOUSE:
            second_opponent = MouseMonitor(2, video_analyzer, reward_manager)
        elif opponent_configuration.get("opponent2_type") == OpponentType.FIXED_STRATEGY:
            second_opponent = FixedStrategyPrisoner(opponent_configuration.get("opponent2_strategy"), opponent_configuration.get("opponent2_probability"))
        else:
            second_opponent = Simulated_mouse()

        # Initialize and start the experiment
        expManager = ExperimentManager(video_analyzer, reward_manager)
        print("Experiment manager now running")
        expManager.start_streaming_exp(experiment_parameters, first_opponent, second_opponent)
        del expManager
    else:
        print("No valid settings were provided.")

# Run the main function
if __name__ == "__main__":
    main()

