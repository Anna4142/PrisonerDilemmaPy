import random
from collections import defaultdict
from Video_analyser_code.locations import Locations
from State_manager_code.StateManager import States
class QLearningAgent:
    def __init__(self):
        # Initialize Q-learning parameters with default values (can be set later)
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1

        # Initialize the action space
        self.action_space = [location for location in Locations if location != Locations.Unknown]


        # Initialize the Q-table with all state-action pairs set to 0.0
        self.q_table = defaultdict(lambda: defaultdict(float))
        for state in States:
            for action in Locations:
                self.q_table[state][action] = 0.0

    def set_parameters(self, learning_rate, discount_factor, epsilon, action_space):
        """
        Set the parameters for the Q-learning agent.
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.action_space = action_space

    def choose_action(self, state):
        """
        Choose an action based on the current state using the epsilon-greedy policy.
        """
        if random.random() < self.epsilon:
            # Explore: choose a random action
            action = random.choice(self.action_space)
        else:
            # Exploit: choose the best known action
            max_q_value = max(self.q_table[state].values(), default=0)
            actions_with_max_q = [action for action in self.action_space if self.q_table[state][action] == max_q_value]
            action = random.choice(actions_with_max_q) if actions_with_max_q else random.choice(self.action_space)

        # Print the chosen action
        print(f"Chosen action for state {state}: {action}")
        return action

    def learn(self, state, action, reward, next_state):
        """
        Update the Q-table based on the action taken, the reward received, and the next state.
        """
        print("IN LEARN")
        print(self.q_table)
        print("next_state",next_state)
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values(), default=0)
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state][action] = new_value

    def get_q_table(self):
        """
        Returns the current Q-table. Useful for debugging or analysis.
        """
        print(self.q_table)
        return dict(self.q_table)
"""""
The __init__ method sets up the Q-learning agent with default parameters and initializes an empty Q-table.
set_parameters is a method to update the agent's learning parameters and action space. This should be called before using the agent for learning.
choose_action implements the epsilon-greedy policy for action selection. It either explores a random action or exploits the best action based on the Q-table.
learn updates the Q-table using the standard Q-learning formula. It's called after each action to learn from the experience.
get_q_table is a utility method to access the current state of the Q-table, which can be useful for analysis or debugging.

"""""
