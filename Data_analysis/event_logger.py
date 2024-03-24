import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger
import pandas as pd

class EventLogger(BaseLogger):
    def __init__(self):
        super().__init__()
        self.temp_data = []  # Temporary storage for events
        self.current_trial_started = False  # Flag to track if a trial has started

    def start_logging(self):
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.EXPERIMENT_EVENT_LOG) + '.csv'
        header = ["Trial Number", "Event", "Time", "Event Number", "Time in State"]
        self._create_file(self.csv_file_path, header)

    def log_data(self, trial_number, event,event_number, time):
        # Check if the event is 'States.TrialStarted'

        self.temp_data.append([trial_number, event, time, event_number, time])  # Time in State is None for now

    def finalize_logging(self):
        # Process temp_data to calculate 'Time in State' and save to CSV

        df.to_csv(self.csv_file_path, index=False)
        print(f"Event logging finalized and saved to {self.csv_file_path}")
