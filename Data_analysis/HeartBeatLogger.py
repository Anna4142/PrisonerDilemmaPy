import Data_analysis.FileUtilities as fUtile
from Data_analysis.LoggerABC import BaseLogger

class HeartBeatLogger(BaseLogger):
    def __init__(self, oppid):
        super().__init__()
        self.csv_file_path = fUtile.get_file_path(fUtile.FileType.HEART_BEAT, 1) + '.csv'

    def start_logging(self):
        header = ["Time Stamp"]
        self._create_file(header)

    def log_data(self, hb_time):
        self._log_data([hb_time])

