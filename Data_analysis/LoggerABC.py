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

    @abstractmethod
    def log_data(self, data):
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerow(data)

    #def get_csv_file_path(self):
    #    return self.csv_file_path

    def _create_file(self, path, header):
        self.csv_file_path = path
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            self.csv_writer = csv.writer(csvfile)
            self.csv_writer.writerow(header)
        print(f"Logging started, file created at: {path}")

    def finalize_logging(self):
        #self.csv_file.close()
        pass

