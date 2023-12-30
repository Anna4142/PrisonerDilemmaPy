from abc import ABC, abstractmethod

class Prisoner (ABC):

    @abstractmethod
    def getDecision(self, zones_list):
        pass

    @abstractmethod
    def NewTrial(self):
        pass

    @abstractmethod
    def DeliverReward(self, opponent_decision, reward_time):
        pass