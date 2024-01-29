import csv
import pandas as pd
#from datetime import datetime
from Data_analysis.LoggerABC import BaseLogger
class TrialLogger(BaseLogger):
    def start_logging(self, filename, opponenttype):
        base_path = self._construct_base_file_path(filename, opponenttype)
        folder_path = base_path + 'data_from_trials/'

        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")
        self.csv_file_path = f'{folder_path}{datetime_string}.csv'

        header = ["Trial Number", "Trial Validity", "Opponent Choice", "Mouse Choice", "Reward",
                  "Center Reward", "Opponent Reward", "Opponent Center Reward", "Experiment Start Time",
                  "Time to Make Decision", "Time to Return to Center"]

        self._create_file(self.csv_file_path, header)

    def log_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,
                 mouse_center_reward, opponent_reward, opponent_center_reward, time_start,
                 time_to_make_decision, time_to_return_to_center):
        data = [trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,
                mouse_center_reward, opponent_reward, opponent_center_reward, time_start,
                time_to_make_decision, time_to_return_to_center]
        super().log_data(data)


"""""
class TrialLogger:
    def __init__(self):
        self.csv_file = None
        self.csv_file_path=None

    def start_logging(self, filename, opponenttype):
        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")
        if opponenttype=="MOUSE_COMPUTER" :
            self.csv_file_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/data_from_trials/{datetime_string}.csv'
        elif opponenttype=="COMPUTER_COMPUTER" :
            self.csv_file_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/data_from_trials/{datetime_string}.csv'
       
        self.csv_file = open(self.csv_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)

        # Include new headers for timing data

        self.csv_writer.writerow(["Trial Number", "Trial Validity", "Opponent Choice", "Mouse Choice", "Reward","Center Reward", "Opponent Reward","Opponent Center Reward", "Experiment Start Time", "Time to Make Decision", "Time to Return to Center"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,mouse_center_reward, opponent_reward, opponent_center_reward,time_start, time_to_make_decision, time_to_return_to_center):
        # Include new data points in the row
        print("logging")
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward, mouse_center_reward,opponent_reward, opponent_center_reward,time_start, time_to_make_decision, time_to_return_to_center])

    def get_csv_file_path(self):
        return self.csv_file_path

    def finalize_logging(self):
        self.csv_file.close()
"""""