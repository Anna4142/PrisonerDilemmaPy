import csv
import Data_analysis.FileUtilities as fUtile


class TrialLogger:
    def __init__(self):
        self.csv_file = None
        self.csv_file_path = None
        self.csv_writer = None

    def start_logging(self):
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_LOG) + '.csv'
        self.csv_file = open(self.csv_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)

        # Write file headers
        print("writing to csv")
        self.csv_writer.writerow(["Trial Number", "Trial Validity", "Opponent Choice", "Mouse Choice", "Reward","Center Reward", "Opponent Reward","Opponent Center Reward", "Experiment Start Time", "Time to Make Decision", "Time to Return to Center"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,mouse_center_reward, opponent_reward, opponent_center_reward,time_start, time_to_make_decision, time_to_return_to_center):
        # Include new data points in the row
        print("logging")
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward, mouse_center_reward,opponent_reward, opponent_center_reward,time_start, time_to_make_decision, time_to_return_to_center])

    def finalize_logging(self):
        self.csv_file.close()