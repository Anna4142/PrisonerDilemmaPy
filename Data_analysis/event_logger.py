import csv
import pandas as pd

class EventLogger:
    def __init__(self):
        self.csv_file = None
        self.csv_file_path = None

    def start_logging(self, filename, opponenttype):
        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")

        # Setting folder path based on opponent type
        if opponenttype == "MOUSE_COMPUTER":
            self.csv_file_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/event_data_from_trials/{datetime_string}.csv'
        elif opponenttype == "COMPUTER_COMPUTER":
            self.csv_file_path = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/event_data_from_trials/{datetime_string}.csv'



        self.csv_file = open(self.csv_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)


        self.csv_writer.writerow(["Trial Number", "Event", "Time"])
        print("Event logging started, file created at:", self.csv_file_path)

    def log_event_data(self, trial_number, event, time):

        self.csv_writer.writerow([trial_number, event, time])
        print(f"Event logged: Trial {trial_number}, Event: {event}, Time: {time}")

    def get_csv_file_path(self):
        return self.csv_file_path