import csv
import Data_analysis.FileUtilities as fUtile


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

    def finalize_logging(self):
        self.csv_file.close()