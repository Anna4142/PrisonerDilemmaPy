import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger

class TrialLogger(BaseLogger):
    def start_logging(self):
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_LOG) + '.csv'

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

