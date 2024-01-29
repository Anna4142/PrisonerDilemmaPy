import csv
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

    def start_logging(self, filename, opponenttype):
        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")

        # Setting folder path based on opponent type
        if opponenttype == "MOUSE_COMPUTER":
            folder_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/event_data_from_trials/'
        elif opponenttype == "COMPUTER_COMPUTER":
            folder_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/event_data_from_trials/'


        self.csv_file_path = f'{folder_path}{datetime_string}.csv'

        with open(self.csv_file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            # Headers for event data
            csv_writer.writerow(["Trial Number", "Event", "Time"])
        print("Event logging started, file created at:", self.csv_file_path)

    def log_event_data(self, trial_number, event, time):
        with open(self.csv_file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([trial_number, event, time])
        print(f"Event logged: Trial {trial_number}, Event: {event}, Time: {time}")

    def get_csv_file_path(self):
        return self.csv_file_path
"""""