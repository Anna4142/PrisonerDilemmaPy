import torch
import torch.nn as nn
import torch.optim as optim
from statemanager.StateManager import  *
import torch.nn.functional as F

import random

from collections import deque
import random
class PolicyNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(PolicyNetwork, self).__init__()
        # Define the architecture of the neural network here
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        action_probs = self.softmax(self.fc3(x))
        return action_probs
class ValueNetwork(nn.Module):
    def __init__(self, state_size):
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        value = self.fc3(x)
        return value

class ActorCriticAgent:
    def __init__(self):
        self.state_manager = StateManager()
        self.state_size = 1
        self.action_size = self.state_manager.get_action_size()

        self.policy_network = PolicyNetwork(self.state_size, self.action_size)
        self.value_network = ValueNetwork(self.state_size)

        self.optimizer_policy = optim.Adam(self.policy_network.parameters(), lr=0.00001)
        self.optimizer_value = optim.Adam(self.value_network.parameters(), lr=0.00001)

        self.gamma = 0.99
        self.states, self.actions, self.rewards = [], [], []

    def remember(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

    def choose_action(self, state):
        state = torch.from_numpy(np.array([state])).float()
        action_probs = self.policy_network(state)
        action = torch.multinomial(action_probs, 1).item()
        return action

    def update_policy(self):
        returns = []
        G = 0
        for reward in reversed(self.rewards):
            G = reward + self.gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns)
        values = torch.cat([self.value_network(torch.from_numpy(np.array([state])).float()) for state in self.states])

        advantages = returns - values.detach().squeeze()

        self.optimizer_policy.zero_grad()
        self.optimizer_value.zero_grad()

        for (state, action, advantage, return_) in zip(self.states, self.actions, advantages, returns):
            state = torch.from_numpy(np.array([state])).float()
            action_probs = self.policy_network(state)
            log_prob = torch.log(action_probs.squeeze(0)[action])
            actor_loss = -log_prob * advantage

            value = self.value_network(state)
            critic_loss = F.mse_loss(value.squeeze(), return_)

            total_loss = actor_loss + critic_loss
            total_loss.backward()

        self.optimizer_policy.step()
        self.optimizer_value.step()

        self.states, self.actions, self.rewards = [], [], []