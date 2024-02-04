import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger


class EventLogger(BaseLogger):
    def start_logging(self):
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_EVENT_LOG) + '.csv'
        header = ["Trial Number", "Event", "Time"]
        self._create_file(self.csv_file_path, header)

    def log_data(self, trial_number, event, time):
        data = [trial_number, event, time]
        super().log_data(data)