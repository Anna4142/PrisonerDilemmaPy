import csv
import pandas as pd
from abc import ABC, abstractmethod
import os
class BaseLogger(ABC):
    def __init__(self):
        self.csv_file = None
        self.csv_file_path = None

    def _construct_base_file_path(self, filename, opponenttype):
        # Construct and return the base file path
        #return f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/'
        if opponenttype == "MOUSE_COMPUTER":
            return f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/'
        elif opponenttype == "COMPUTER_COMPUTER":
            return  f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/'


    @abstractmethod
    def start_logging(self, filename, opponenttype):
        pass

    @abstractmethod
    def log_data(self, data):
        with open(self.csv_file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)


    def get_csv_file_path(self):
        return self.csv_file_path

    def _create_file(self, path, header):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)
        print(f"Logging started, file created at: {path}")

