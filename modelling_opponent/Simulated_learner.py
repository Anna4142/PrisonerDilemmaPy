import random
#from VideoAnalyzerStub import Video_Analyzer
from State_manager_code.StateManager import States
from locations import Locations
from models.Learning_agents.qlearner import QLearningAgent
class Simulated_mouse:
    def __init__(self):
        self.strategy = "Unconditional Cooperator"
        self.LastDecision = Locations.Center
        self.p = 0.5  # Default value for probability
        self.decisionMade = True
        self.rewardReceived = True
        self.q_learning_agent = None  # Initialize as None

    def SetStrategy(self, strategy):
        self.strategy = strategy
        if strategy == "Q-Learner":
            # Initialize or reset the Q-learning agent
            self.q_learning_agent = QLearningAgent()

    def NewTrial(self):
        self.decisionMade = False
        self.rewardReceived = False

    def setRewardReceived(self):
        self.rewardReceived = True


    def get_mouse_location(self, mouse_location,current_state):