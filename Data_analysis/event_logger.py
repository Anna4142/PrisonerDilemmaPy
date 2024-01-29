import csv
import Data_analysis.FileUtilities as fUtile
import pandas as  pd
from Data_analysis.LoggerABC import BaseLogger
class EventLogger(BaseLogger):
    def start_logging(self, filename, opponenttype):
        base_path = self._construct_base_file_path(filename, opponenttype)
        folder_path = base_path + 'event_data_from_trials/'

        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")
        self.csv_file_path = f'{folder_path}{datetime_string}.csv'

        header = ["Trial Number", "Event", "Time"]
        self._create_file(self.csv_file_path, header)

    def log_data(self, trial_number, event, time):
        data = [trial_number, event, time]
        super().log_data(data)

"""""
class EventLogger:
    def __init__(self):
        self.csv_file = None
        self.csv_file_path = None
        self.csv_writer = None

    def start_logging(self):
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_EVENT_LOG) + '.csv'
        self.csv_file = open(self.csv_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)

        # Write file headers
        #print("writing to csv")
        self.csv_writer.writerow(["Trial Number", "Event", "Time"])

    def log_event_data(self, trial_number, event, time):
        self.csv_writer.writerow([trial_number, event, time])
        #print(f"Event logged: Trial {trial_number}, Event: {event}, Time: {time}")

"""""
