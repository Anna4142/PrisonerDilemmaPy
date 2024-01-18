from Experiment_Launcher_code.ModuleConfiguration import __USE_VIDEO_SIM
from Experiment_Launcher_code.ModuleConfiguration import __USE_VIDEO_STUB
if __USE_VIDEO_SIM:
    from Video_analyser_code.VideoAnalyzerSim import Video_Analyzer
elif __USE_VIDEO_STUB:
    from Video_analyser_code.VideoAnalyzerStub import Video_Analyzer
else:
    from Video_analyser_code.VideoAnalyser import Video_Analyzer

from modelling_opponent.MouseMonitor import MouseMonitor
from modelling_opponent.FixedStrategyPrisoner import FixedStrategyPrisoner
#from modelling_opponent.Simulated_learner import Simulated_mouse
from Reward_manager.RewardManager import RewardManager
from Experiment_Launcher_code.ExperimentManager import ExperimentManager
from Experiment_Launcher_code.experimentgui import ExperimentGUI, OpponentType
from Data_analysis.DataAnalysisScript import DataAnalyzer

def main():
    # Create an instance of the ExperimentGUI class
    experiment_gui = ExperimentGUI()
    experiment_gui.setup_gui()

    # After the GUI is closed, get the settings using the appropriate methods
    if experiment_gui.experiment_started():
        comport_name = experiment_gui.get_com_port()
        experiment_parameters = experiment_gui.get_experiment_parameters()
        opponent_configuration = experiment_gui.get_opponent_configuration()
        if opponent_configuration.get("opponent1_type") == OpponentType.MOUSE:
            opponent_path = "MOUSE_COMPUTER"
        else:
            opponent_path = "COMPUTER_COMPUTER"

        # Instantiate software components
        video_analyzer = Video_Analyzer(experiment_parameters.get("mouse_id"), opponent_path)
        reward_manager = RewardManager(comport_name)

        # Configure Opponents
        if opponent_configuration.get("opponent1_type") == OpponentType.MOUSE:
            first_opponent = MouseMonitor(1, video_analyzer, reward_manager)
        elif opponent_configuration.get("opponent1_type") == OpponentType.FIXED_STRATEGY:
            first_opponent = FixedStrategyPrisoner(opponent_configuration.get("opponent1_strategy"), opponent_configuration.get("opponent1_probability"))
        else:
            pass #first_opponent = Simulated_mouse()

        if opponent_configuration.get("opponent2_type") == OpponentType.MOUSE:
            second_opponent = MouseMonitor(2, video_analyzer, reward_manager)
        elif opponent_configuration.get("opponent2_type") == OpponentType.FIXED_STRATEGY:
            second_opponent = FixedStrategyPrisoner(opponent_configuration.get("opponent2_strategy"), opponent_configuration.get("opponent2_probability"))
        else:
            pass #second_opponent = Simulated_mouse()

        # Initialize and start the experiment
        expManager = ExperimentManager(video_analyzer, reward_manager)
        print("Experiment manager now running")
        expManager.start_streaming_exp(experiment_parameters, first_opponent, second_opponent, opponent_path)
    
        data_file_path = expManager.get_data_file_path()  # Get the path of the logged data

        # Initialize DataAnalyzer with the file path
        data_analyzer = DataAnalyzer(data_file_path)

        # Perform data analysis
        analysis_results = data_analyzer.analyze_data()

        # Save analysis results
        result_file_path = data_analyzer.save_results_to_file(analysis_results)
        print(f"Analysis results saved to {result_file_path}")
        del expManager
    else:
        print("No valid settings were provided.")

# Run the main function
if __name__ == "__main__":
    main()

