import csv
import pandas as pd

class TrialLogger:
    def __init__(self):
        self.csv_file = None

    def start_logging(self, filename):
        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d")
        filepath = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/data_from_trials/{filename}.csv'

        self.csv_file = open(filepath, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        # Include new headers for timing data
        self.csv_writer.writerow(["Trial Number", "Trial Validity", "Opponent Choice", "Mouse Choice", "Reward", "Opponent Reward", "Experiment Start Time", "Time to Make Decision", "Time to Return to Center"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward, opponent_reward, time_start, time_to_make_decision, time_to_return_to_center):
        # Include new data points in the row
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward, opponent_reward, time_start, time_to_make_decision, time_to_return_to_center])

    def finalize_logging(self):
        self.csv_file.close()