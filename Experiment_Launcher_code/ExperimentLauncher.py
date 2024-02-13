from Data_analysis.DataAnalysisScript import DataAnalyzer
import os
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
import Data_analysis.FileUtilities as fUtile
from  Data_analysis.EventComparison import EventComparator
from  Data_analysis.Data_analysis_plots import DataPlotter


def main():
    # Create an instance of the ExperimentGUI class
    experiment_gui = ExperimentGUI()
    experiment_gui.setup_gui()

    # After the GUI is closed, get the settings using the appropriate methods
    if experiment_gui.experiment_started():
        comport_name = experiment_gui.get_com_port()
        experiment_parameters = experiment_gui.get_experiment_parameters()
        opponent_configuration = experiment_gui.get_opponent_configuration()

        fUtile.set_file_name(experiment_parameters.get('session_type'), experiment_parameters.get('session_num'))
        write_configuration_file(experiment_parameters, opponent_configuration)

        # Instantiate software components
        video_analyzer = Video_Analyzer()
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
        expManager.start_streaming_exp(experiment_parameters, first_opponent, second_opponent)
    
        data_file_path =fUtile.get_file_path(fUtile.FileType.EXPERIMENT_LOG) + '.csv'  # Get the path of the logged data

        data_analyzer = DataAnalyzer(data_file_path)
        # Perform data analysis
        analysis_results = data_analyzer.analyze_data()
        # Save analysis results
        data_analysis_file_path = fUtile.get_file_path(fUtile.FileType.DATA_ANALYSIS) + '.csv'  # Get the path of the logged data
        result_file_path = data_analyzer.save_results_to_file(analysis_results)


        event_csv_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_EVENT_LOG) + '.csv'

        ground_truth_directory="C:/Users/anush/Downloads/Experiment_Folder/Ground_Truth_Data/StrategyData"
        comparator = EventComparator(ground_truth_directory, event_csv_path)
        comparator.save_scores()
        # Initialize DataAnalyzer with the file path


        save_directory = fUtile.get_file_path(fUtile.FileType.DATA_ANALYSIS_PLOTS) # Specify your custom save directory here

        plotter = DataPlotter(data_file_path, save_directory)
        plotter.load_data()
        plotter.filter_completed_trials()
        plotter.plot_decision_time()  # This will now save to the specified directory
        plotter.plot_return_time()

        print(f"Analysis results saved to {result_file_path}")
        del expManager
    else:
        print("No valid settings were provided.")


def write_configuration_file(experiment_parameters, opponent_configuration):
    filepath = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_CONFIGURATION) + ".txt"
    with open(filepath, 'w') as file:
        file.write('Experiment name: ' + experiment_parameters.get('experiment_name') + '\n')
        file.write('Session Type & number: ' + experiment_parameters.get('session_type') + ', ' + experiment_parameters.get('session_num') + '\n')
        file.write('Number of Trials: ' + str(experiment_parameters.get('num_trials')) + '\n')
        file.write('Decision and Return Time limits: ' + str(experiment_parameters.get('decision_time')) + ', ' + str(experiment_parameters.get('return_time')) + '\n')
        write_opponent_configuration(file, opponent_configuration, 'First')
        write_opponent_configuration(file, opponent_configuration, 'Second')


def write_opponent_configuration(file, configuration, oppid):
    oppnum = '1'
    if oppid == 'Second':
        oppnum = '2'
    otype = 'opponent1_type'.replace('1', oppnum)
    mouseid = 'mouse_1_id'.replace('1', oppnum)
    ostrategy = 'opponent1_strategy'.replace('1', oppnum)
    oprobability = 'opponent1_probability'.replace('1', oppnum)

    if configuration.get(otype) == OpponentType.MOUSE:
        file.write(f'{oppid} Opponent: Mouse, Mouse ID: {configuration.get(mouseid)}\n')
    elif configuration.get(otype) == OpponentType.FIXED_STRATEGY:
        if configuration.get(ostrategy) == 'Probability p Cooperator':
            file.write(f'{oppid} Opponent: Fixed Strategy: {configuration.get(ostrategy)}, Probability: {str(configuration.get(oprobability))}\n')
        else:
            file.write(f'{oppid} Opponent: Fixed Strategy: {configuration.get(ostrategy)}\n')
    else:
        file.write(f'{oppid} Opponent: Learner. \n')


# Run the main function
if __name__ == "__main__":
    main()

