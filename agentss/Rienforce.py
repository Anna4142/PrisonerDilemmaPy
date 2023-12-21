
import numpy as np
from statemanager.StateManager import  *
class reinforce_agent:
    def __init__(self):
        self.state_manager=StateManager()
        self.state_size = self.state_manager.get_state_size()
        self.action_size = self.state_manager.get_action_size()

        # Policy table
        self.policy_table = np.ones((self.state_size, self.action_size)) / self.action_size

        # Discount rate
        self.gamma = 0.99

        # Store states, actions and rewards
        self.states, self.actions, self.rewards = [], [], []

    def remember(self, state, action, reward):
        """Stores state, action, and reward."""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

    def choose_action(self, state):
        # Convert state to integer if it's not already
        if isinstance(state, Enum):
            state_index = state.value
        else:
            state_index = int(state)  # Ensuring state is an integer

        # Ensure state_index is within the valid range
        if state_index >= len(self.policy_table):
            raise IndexError("State index out of range")

        action_probs = self.policy_table[state_index]
        action = np.random.choice(self.action_size, p=action_probs)
        #print(self.policy_table)
        return action
    def update_policy(self):
        """Updates the policy based on accumulated states, actions, and rewards."""
        G = 0
        for state, action, reward in zip(reversed(self.states), reversed(self.actions), reversed(self.rewards)):
            if isinstance(state, Enum):
                state_index = state.value
            else:
                state_index = int(state)  # Ensuring state is an integer

            print("state",state)
            print("action",action)
            print("reward",reward)

            G = reward + self.gamma * G
            # Update policy for the state-action pair
            print("g", G)
            self.policy_table[state_index, action] *= G
            self.policy_table[state_index] /= np.sum(self.policy_table[state_index])

            print(self.policy_table)
        # Clear memory
        self.states, self.actions, self.rewards = [], [], []

"""""

1. Define the Policy
Since you prefer not using neural networks, your policy could be a probability distribution over actions for each state. This can be represented as a table where rows correspond to states and columns to actions.

2. Collect Episode Trajectories
For each episode, let the agent interact with the environment using the current policy, and collect the entire trajectory of states, actions, and rewards.

3. Calculate the Return
For each step in an episode, calculate the return (total discounted future reward) from that step onwards.

4. Policy Gradient Update
Adjust the policy in a way that increases the likelihood of actions that lead to higher returns. In a tabular setting, this could involve increasing the probability of the taken actions proportionally to their returns.
"""