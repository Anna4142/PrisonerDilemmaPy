# Mikcy: The MainWindow file name is a bit of a mis nomenclature. it a left over from the old code where this module actually lanuceched
#        the main gui window. I know this sounds like a pure nuisance but remember a code is written only once and used (read, maintained, changed)
#        by generations of programmers. Names are important for understanding. Care to try another name?
from ExperimentManager1 import ExperimentManager
from experimentgui import ExperimentGUI, OpponentType     # Micky: I do not understand how this works. OpponenType is not defined in experimentGui

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

        # Adjust logic based on enum                   # Micky: The if structure is redundant. you are doing the exact same thing for all cases.
        if opponent_type == OpponentType.MOUSE_COMPUTER:
            opponent_strategy_1 = settings.get('opponent_strategy')
            opponent_strategy_2 = settings.get('computer_opponent_strategy')
        elif opponent_type == OpponentType.COMPUTER_COMPUTER:
            opponent_strategy_1 = settings.get('opponent_strategy')
            opponent_strategy_2 = settings.get('computer_opponent_strategy')
        else:
            # Handle other types or default
            opponent_strategy_1 = settings.get('opponent_strategy')
            opponent_strategy_2 = settings.get('computer_opponent_strategy')

        # Modify num_trials as per your requirement
        num_trials += 2                               # Micky: I assume this is solved in the next version.

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