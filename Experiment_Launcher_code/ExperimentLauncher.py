from Experiment_Launcher_code.ExperimentManager import ExperimentManager
from Experiment_Launcher_code.experimentgui import ExperimentGUI, OpponentType

def main():
    # Create an instance of the ExperimentGUI class
    experiment_gui = ExperimentGUI()
    experiment_gui.setup_gui()

    # After the GUI is closed, get the settings using the get_settings method
    settings = experiment_gui.on_start_clicked()

    if settings:
        # Extract the necessary parameters from the settings
        num_trials = settings.get('num_trials')
        trial_duration = settings.get('trial_duration')
        decision_time = settings.get('decision_time')

        opponent_type = settings.get('opponent_type')  # This should now be an OpponentType enum value
        opponent_strategy_1 = settings.get('opponent_strategy')
        opponent_strategy_2 = settings.get('computer_opponent_strategy')
        # Adjust logic based on enum

        num_trials += 2

        # Initialize and start the experiment
        expManager = ExperimentManager()
        print("Experiment manager now running")
        expManager.start_streaming_exp(num_trials, trial_duration, decision_time, opponent_type, opponent_strategy_1, opponent_strategy_2)
        del expManager
    else:
        print("No valid settings were provided.")

# Run the main function
if __name__ == "__main__":
    main()