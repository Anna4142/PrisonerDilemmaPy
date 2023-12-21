import random
from opponent.MouseMonitor import MouseMonitor
from statemanager.StateManager import StateManager
from statemanager.StateManager import States
from statemanager.locations import Locations
from agentss.qlearner import QLearningAgent
from agentss.ActorCritic  import ActorCriticAgent
from agentss.Rienforce  import reinforce_agent
from agentss.ReinforceAgent import ReinforceAgent

class Simulated_mouse:
    def __init__(self, data_queue, mouse_id):
            self.strategy = "Unconditional Cooperator"
            self.data_queue = data_queue  # Use the passed-in shared queue
            self.LastDecision = Locations.Center
            self.p = 0.5  # Default probability value
            self.mouse_monitor = MouseMonitor(data_queue, mouse_id)  # Use the same queue
            self.decisionMade = True
            self.rewardReceived = True
            self.q_learning_agent = QLearningAgent()
            self.actor_critic_agent=ActorCriticAgent()
            self.reinforce_agent=ReinforceAgent()
            self.state_manager=StateManager()
            self.reward=0

    def SetStrategy(self, strategy):

        self.strategy = strategy
        print("strategy", self.strategy)

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




    def GetMouseLocation(self, mouse_location,current_state,id):

           if self.strategy == "actor_critic":
                # Use the Actor to choose an action
                action = self.actor_critic_agent.choose_action(current_state)
                mouse_location = Locations.map_enum_to_location(action)

                # Determine the next state and reward based on the action
                next_state = self.state_manager.NextState[current_state]
                reward_function = self.state_manager.RewardCalculation.get(current_state, lambda _: 0)
                self.reward = reward_function(action)

                # Update the Actor-Critic agent
                self.actor_critic_agent.learn(current_state, action, self.reward, next_state)

                return mouse_location
           elif self.strategy == "reinforce":
                # Convert current state to the appropriate format for NN input
                formatted_current_state = self.state_manager.get_current_state_as_numpy(current_state)

                # Choose action based on the current state
                action = self.reinforce_agent.choose_action(formatted_current_state)

                mouse_location = Locations.map_num_to_location(action)

                print("current state",current_state)
                # Determine the next state and reward
                next_state =self.state_manager.NextState[current_state]
                reward_function = self.state_manager.RewardCalculation.get(current_state, lambda _: 0)
                self.reward = reward_function(action)

                # Remember the experience
                self.reinforce_agent.remember(formatted_current_state, action, self.reward)

                # Check if the episode has ended, then update the policy
                if current_state == States.End :  # Add condition to determine the end of an episode
                    self.reinforce_agent.update_policy()

                # Update current state
                current_state=next_state

                return mouse_location
           elif self.strategy == "q learner" and self.q_learning_agent is not None:
                list_opp = self.q_learning_agent.choose_action(current_state)
                mouse_location = Locations.map_enum_to_location(list_opp)
                #print("q learner choice",list_opp)
                #print("q learner choice", mouse_location)
                next_state = self.state_manager.NextState[current_state]
                #print("CURRENT STATE",current_state)
                #print("NEXT STATE", next_state)
                # Calculate the reward based on the action and state
                #reward = self.calculate_reward(current_state, list_opp)
                reward_function = self.state_manager.RewardCalculation.get(current_state, lambda _: 0)
                self.reward = reward_function(list_opp)
                next_max= self.q_learning_agent.learn(current_state, list_opp, self.reward, next_state)
                #print("NEXT MAX", next_max)
                self.q_learning_agent.get_q_table(id,next_max)



                return mouse_location  ##returns list to specify mouses location




            #if self.strategy != "q learner":
           list_opp = [0, 1, 0]  # Default to no decision


           if not mouse_location:  # If the mouse_location isn't provided, get it from the MouseMonitor
                mouse_location = self.mouse_monitor.get_mouse_location()

           if current_state == States.Start:
                list_opp = [0, 1, 0]  # Example: Cooperate

           elif current_state == States.CenterReward:
                list_opp = [0, 1, 0]  # Example: Move to Center

           elif current_state == States.TrialStarted:
                # Decision-making based on the strategy
                # Existing logic based on strategy goes here

                if self.strategy == "Unconditional Cooperator":
                    list_opp = [1, 0, 0]  # Cooperate in these states

                elif self.strategy == "Unconditional Defector":
                    list_opp = [0, 0, 1]  # Defect in these states

                elif self.strategy == "Random":
                    list_opp = random.choice([[1, 0, 0], [0, 0, 1]])  # Randomly choose between Cooperate and Defect

                elif self.strategy == "Probability p Cooperator":
                    list_opp = [1, 0, 0] if random.random() < self.p else [0, 0, 1]  # Cooperate based on probability p

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
                list_opp = [0, 1, 0]  # Example: Move to Center

           elif current_state == States.TrialCompleted:
                list_opp = [0, 1, 0]
           elif current_state == States.TrialAbort:
                list_opp = [0, 1, 0]

           elif current_state == States.DecisionAbort:
                list_opp = [0, 1, 0]  # Example: Move to Center

           elif current_state == States.End:
                list_opp = [0, 0, 0]  # Example: Defect

           return list_opp
