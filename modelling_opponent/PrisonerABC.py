from abc import ABC, abstractmethod

class Prisoner (ABC):

    @abstractmethod
    def getDecision(self, zones_list):
        pass

    @abstractmethod
    def NewTrial(self):
        pass

    @abstractmethod
    def DeliverReward(self, reward_time):
        pass