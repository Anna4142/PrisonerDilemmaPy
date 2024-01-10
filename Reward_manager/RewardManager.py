# Use the Arduino import statement to select between real and simulated HW
from Arduino_related_code.ArduinoDigital import ArduinoDigital
#from Arduino_related_code.ArduinoDigitalSim import ArduinoDigital

from Arduino_related_code.ValveControl import ValveControl
from Video_analyser_code.locations import Locations


class RewardManager:
    def __init__(self, comport):
        self.board = ArduinoDigital(comport)
        self.valves = [ValveControl(channel, self.board) for channel in [7, 8, 9, 10, 11, 12]]
        self.reward_mapping = {
            'first_prisoner': {Locations.Cooperate : 5, Locations.Center : 4, Locations.Defect : 3},
            'second_prisoner': {Locations.Cooperate : 2, Locations.Center : 1, Locations.Defect : 0}}

    def deliver_reward(self, mouse_id, location, reward_time):
        if mouse_id == 1:
            valve_map = self.reward_mapping.get('first_prisoner', {})
        else:
            valve_map = self.reward_mapping.get('second_prisoner', {})
        valveindex = valve_map.get(location)
        if valveindex is None:
            valveindex=4
        self.valves[valveindex].OpenValve(reward_time)

    def is_reward_delivered(self):
        rewarDelivered = True
        for valve in self.valves:
            if valve.IsValveOpen():
                rewarDelivered = False
        return rewarDelivered