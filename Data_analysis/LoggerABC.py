import csv
from abc import ABC, abstractmethod
import os


class BaseLogger(ABC):
    def __init__(self):
        self.csv_file = None
        self.csv_file_path = None
        self.csv_writer = None

    @abstractmethod
    def start_logging(self):
        pass

    def _log_data(self, data):
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerow(data)

    def _create_file(self, header):
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerow(header)
        print(f"Logging started, file created at: {self.csv_file_path}")

    def finalize_logging(self):
        pass

