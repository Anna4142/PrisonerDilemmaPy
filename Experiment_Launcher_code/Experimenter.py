class Experimenter:
    def __init__(self, video_analyzer):
        self.video_analyzer = video_analyzer


    def check_for_start(self):
        # Check if the experimenter's zone is activated
        if self.video_analyzer.get_exp_zone_activations()==1:
            print("STARTING THE EXPERIMENT NOW")

            return True  # Return True if the experimenter's zone is activated
        else:
            return False  # Return False otherwise