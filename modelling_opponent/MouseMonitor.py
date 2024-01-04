from Video_analyser_code.locations import Locations
from modelling_opponent.PrisonerABC import Prisoner

class MouseMonitor(Prisoner):
    def __init__(self, mouse_id, video_analyzer, reward_manager):
        self.mouse_id = mouse_id
        self.mouse_location = Locations.Unknown
        self.video_analyser = video_analyzer
        self.reward_manager = reward_manager

    def getDecision(self, zones_list,state):
        # Split the zones based on mouse_id
        mouse_zones = zones_list[(self.mouse_id - 1) * 3 : self.mouse_id * 3]

        # Interpret the zones list to return the corresponding location
        location = Locations.Unknown
        if mouse_zones[0] == 1:
            location = Locations.Cooperate
        elif mouse_zones[1] == 1:
            location = Locations.Center
        elif mouse_zones[2] == 1:
            location = Locations.Defect

        self.mouse_location = location
        return location

    def NewTrial(self):
        pass

    def DeliverReward(self, opponent_decision, reward_time):
        self.reward_manager.deliver_reward(self.mouse_id, self.mouse_location, reward_time)



