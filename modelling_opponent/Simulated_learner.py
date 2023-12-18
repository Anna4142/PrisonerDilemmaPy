import random
#from VideoAnalyzerStub import Video_Analyzer
from State_manager_code.StateManager import States
from State_manager_code.StateManager import StateManager
from Video_analyser_code.locations import Locations
from models.Learning_agents.qlearner import QLearningAgent
class Simulated_mouse:
    def __init__(self):
        self.strategy = "Unconditional Cooperator"
        self.LastDecision = Locations.Center
        self.p = 0.5  # Default value for probability
        self.decisionMade = True
        self.rewardReceived = True
        self.q_learning_agent = QLearningAgent()
        self.state_manager=StateManager()

    def SetStrategy(self, strategy):
        self.strategy = strategy

    def NewTrial(self):
        self.decisionMade = False
        self.rewardReceived = False

    def setRewardReceived(self):
        self.rewardReceived = True

    def setProbability(self, p):
        """Method to set the probability value for 'Probability p Cooperator' strategy"""
        if 0 <= p <= 1:
            self.p = p
        else:
            print("Error: p should be between 0 and 1")

    def update_and_print_q_table(self, current_state, action, reward, next_state):
            """Update the Q-table and print it."""
            self.q_learning_agent.learn(current_state, action, reward, next_state)
            print("Updated Q-table:")
            print(self.q_learning_agent.get_q_table())  # Assuming there's a method to get the Q-table

    def calculate_reward(self, current_state, action):
        # Initialize reward variable
        reward = 0

        # Reward structure based on current state and action
        if current_state == States.Start:
            reward = 1 if action == Locations.Center else 0

        elif current_state == States.CenterReward:
            reward = 1 if action == Locations.Center else 0

        elif current_state == States.TrialStarted:
            reward = 1 if action == Locations.Center else 0

        elif current_state == States.M1CM2C:
            reward = 3 if action == Locations.Cooperate else -1

        elif current_state == States.M1CM2D:
            reward = -2 if action == Locations.Cooperate else 0

        elif current_state == States.M1DM2C:
            reward = 5 if action == Locations.Defect else -1

        elif current_state == States.M1DM2D:
            reward = 1 if action == Locations.Defect else -1

        elif current_state == States.WaitForReturn:
            reward = 0  # Neutral reward for WaitForReturn state

        elif current_state == States.TrialCompleted:
            reward = 1 if action == Locations.Center else 0

        elif current_state == States.TrialAbort:
            reward = 1 if action == Locations.Center else 0  # Negative reward to avoid this state

        elif current_state == States.DecisionAbort:
            reward = 1 if action == Locations.Center else 0

        elif current_state == States.End:
            reward = 0  # Neutral reward for End state

        # Return the calculated reward
        return reward

    def get_mouse_location(self, current_state):
            # Default action
            list_opp = Locations.Unknown

            if self.strategy == "q learner" and self.q_learning_agent is not None:

                list_opp = self.q_learning_agent.choose_action(current_state)
                next_state = self.state_manager.NextState[current_state]
                print("next state",next_state)
                # Calculate the reward based on the action and state
                reward = self.calculate_reward(current_state, list_opp)
                print("reward",reward)
                # Update the Q-table
                self.update_and_print_q_table(current_state, list_opp, reward, next_state)
            else:
                if current_state == States.Start:
                    list_opp = Locations.Center

                elif current_state == States.CenterReward:
                    list_opp = Locations.Center

                elif current_state == States.TrialStarted:
                    # Decision-making based on the strategy
                    # Existing logic based on strategy goes here

                    if self.strategy == "Unconditional Cooperator":
                        list_opp =Locations.Cooperate # Cooperate in these states

                    elif self.strategy == "Unconditional Defector":
                        list_opp = Locations.Defect  # Defect in these states

                    elif self.strategy == "Random":
                        list_opp = random.choice([Locations.Cooperate,  Locations.Defect ])  # Randomly choose between Cooperate and Defect

                    elif self.strategy == "Probability p Cooperator":
                        list_opp = Locations.Cooperate if random.random() < self.p else Locations.Defect  # Cooperate based on probability p

                    elif self.strategy == "Tit for Tat":
                        # Tit for Tat strategy: Cooperate if opponent cooperated, otherwise defect
                        list_opp = mouse_location

                elif current_state == States.M1CM2C:
                       pass  # Example: Cooperate

                elif current_state == States.M1CM2D:
                        pass # Example: Cooperate

                elif current_state == States.M1DM2C:
                        pass  # Example: Defect

                elif current_state == States.M1DM2D:
                       pass # Example: Defect

                elif current_state == States.WaitForReturn:
                        list_opp = Locations.Center   # Example: Move to Center

                elif current_state == States.TrialCompleted:
                        list_opp = Locations.Center
                elif current_state == States.TrialAbort:
                        list_opp = Locations.Center

                elif current_state == States.DecisionAbort:
                        list_opp =Locations.Center
                elif current_state == States.End:
                        list_opp = Locations.Center

            return list_opp