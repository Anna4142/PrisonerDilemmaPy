from abc import ABC, abstractmethod

class Prisoner (ABC):

    @abstractmethod
    def get_mouse_location(self, zones_list, current_state):
        pass

    @abstractmethod
    def NewTrial(self):
        pass

    @abstractmethod
    def DeliverReward(self, reward):
        pass