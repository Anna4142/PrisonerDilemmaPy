import csv
from datetime import datetime

class TrialLogger:
    def __init__(self):
        self.csv_file = None

    def start_logging(self, filename):
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%Y%m%d-%H%M%S")
        filepath = "./../../ExperimentLogFiles/" + filename + datetime_string + ".csv"
        self.csv_file = open(filepath, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Trial Number", "Trial validity", "Opponent Choice", "Mouse choice", "Reward","opponent Reward"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward):
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward])

    def finalize_logging(self):
        self.csv_file.close()
