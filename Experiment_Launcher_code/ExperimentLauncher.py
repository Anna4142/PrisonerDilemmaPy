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
        experiment_name = settings.get('experiment_name')
        comport_name = settings.get('comport_name')
        num_trials = settings.get('num_trials')
        return_time = settings.get('return_time')
        decision_time = settings.get('decision_time')
        mouse_id=settings.get('mouse_id')
        opponent_type = settings.get('opponent_type')
        opponent1_strategy = settings.get('opponent1_strategy')
        opponent2_strategy = settings.get('opponent2_strategy')
        opponent1_probability = settings.get('opponent1_probability')
        opponent2_probability = settings.get('opponent2_probability')

        # Initialize and start the experiment
        expManager = ExperimentManager(comport_name,mouse_id)
        print("Experiment manager now running")
        expManager.start_streaming_exp(experiment_name, num_trials, decision_time, return_time, opponent_type,
                                       opponent1_strategy, opponent2_strategy)
        del expManager
    else:
        print("No valid settings were provided.")

# Run the main function
if __name__ == "__main__":
    main()

