import random
from modelling_opponent.PrisonerABC import Prisoner
from Video_analyser_code.locations import Locations


class FixedStrategyPrisoner (Prisoner):
    def __init__(self, strategy, probability):
        self.strategy = strategy
        self.LastDecision = Locations.Center
        self.opponentLastDecision = Locations.Cooperate
        self.p = probability
        self.trialStarted = False
        self.decisionMade = False

    def NewTrial(self):
        self.trialStarted = True
        self.decisionMade = False

    def getDecision(self, zones_list):
        if self.trialStarted:
            if self.decisionMade:
                decision = self.LastDecision
            else:
                self.decisionMade = True
                if self.strategy == "Unconditional Cooperator":
                    decision = Locations.Cooperate

                elif self.strategy == "Unconditional Defector":
                    decision = Locations.Defect

                elif self.strategy == "Random":
                    decision = random.choice([Locations.Cooperate,  Locations.Defect ])  # Randomly choose between Cooperate and Defect

                elif self.strategy == "Probability p Cooperator":
                    decision = Locations.Cooperate if random.random() < self.p else Locations.Defect  # Cooperate based on probability p

                elif self.strategy == "Tit for Tat":
                    decision = self.opponentLastDecision # Tit for Tat strategy: Cooperate if opponent cooperated, otherwise defect
        else:
            decision = Locations.Center

        self.LastDecision = decision
        return decision

    def DeliverReward(self, opponent_decision, reward_time):
        if opponent_decision != Locations.Center:
            self.opponentLastDecision = opponent_decision
        self.trialStarted = False
