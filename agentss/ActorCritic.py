import numpy as np
from collections import defaultdict
from statemanager.locations import Locations
from statemanager.StateManager import States

class ActorCriticAgent:
    def __init__(self):
        # Initialize parameters
        self.learning_rate_actor = 0.1
        self.learning_rate_critic = 0.1
        self.discount_factor = 0.9

        # Initialize the action space
        self.action_space = [location for location in Locations if location != Locations.Unknown]

        # Initialize the actor (policy) and critic (value function) tables
        self.actor = defaultdict(lambda: defaultdict(float))
        self.critic = defaultdict(float)
        for state in States:
            for action in self.action_space:
                self.actor[state][action] = 0.0
            self.critic[state] = 0.0

    def choose_action(self, state):
        """
        Choose an action based on the current state using a policy derived from the actor.
        """
        action_probabilities = np.array(list(self.actor[state].values()))
        action_probabilities = np.exp(action_probabilities) / np.sum(np.exp(action_probabilities)) # Softmax
        action = np.random.choice(self.action_space, p=action_probabilities)
        return action

    def learn(self, state, action, reward, next_state):
        """
        Update the actor and critic tables based on the action taken, the reward received, and the next state.
        """
        td_target = reward + self.discount_factor * self.critic[next_state]
        td_error = td_target - self.critic[state]

        # Update critic
        self.critic[state] += self.learning_rate_critic * td_error

        # Update actor
        action_probs = np.exp(list(self.actor[state].values())) / np.sum(np.exp(list(self.actor[state].values())))
        for a in self.action_space:
            if a == action:
                self.actor[state][a] += self.learning_rate_actor * td_error * (1 - action_probs[a])
            else:
                self.actor[state][a] -= self.learning_rate_actor * td_error * action_probs[a]

    def get_policy(self):
        """
        Returns the current policy. Useful for debugging or analysis.
        """
        policy = defaultdict(lambda: defaultdict(float))
        for state, actions in self.actor.items():
            for action, value in actions.items():
                policy[state][action] = np.exp(value) / np.sum(np.exp(list(actions.values())))
        return policy