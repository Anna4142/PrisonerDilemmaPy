import csv
from datetime import datetime
from Experiment_Launcher_code.ExperimentManager import *
class TrialLogger:
    def __init__(self):
        self.csv_file = None

    def start_logging(self, filename):
        filename="1777"
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%Y%m%d-%H%M%S")
        #filepath = "C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/" + filename + datetime_string + ".csv"
        #filepath = "./../../ExperimentLogFiles/" + filename + datetime_string + ".csv"
        base_path = "C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/NEW_EXPERIMENT"
        filepath = f"{base_path}/{ExperimentManager.opponent_type}/data_from_trials/{filename}_{datetime_string}.csv"
        #should be
        ## filepath = f"{base_path}/{ExperimentManager.opponent_type}/data_from_trials/{mouse_id}/{filename}_{datetime_string}.csv"--get the mouse id as an input from the gui

        self.csv_file = open(filepath, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Trial Number", "Trial validity", "Opponent Choice", "Mouse choice", "Reward","opponent Reward"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward):
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward])

    def finalize_logging(self):
        self.csv_file.close()
