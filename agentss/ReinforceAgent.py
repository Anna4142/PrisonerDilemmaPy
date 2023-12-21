import torch
import torch.nn as nn
import torch.optim as optim
from statemanager.StateManager import  *
import numpy as np


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


class ReinforceAgent:
    def __init__(self):
        self.state_manager = StateManager()
        self.state_size = 1
        self.action_size = self.state_manager.get_action_size()
        self.policy_network = PolicyNetwork(self.state_size, self.action_size)
        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=0.00001)
        self.gamma = 0.99
        self.states, self.actions, self.rewards = [], [], []

    def remember(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

    def choose_action(self, states):

        print("states",states)
        state = torch.from_numpy(states).float().unsqueeze(0)
        action_probs = self.policy_network(state)
        print("action probs",action_probs)
        action = torch.multinomial(action_probs, 1).item()
        return action

    def update_policy(self):
        print("UPDATING POLICY")
        returns = []
        G = 0
        for reward in reversed(self.rewards):
            G = reward + self.gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)

        self.optimizer.zero_grad()
        for state, action, G in zip(self.states, self.actions, returns):

            state = torch.from_numpy(state).float().unsqueeze(0)
            action_probs = self.policy_network(state)
            log_prob = torch.log(action_probs.squeeze(0)[action])
            loss = -log_prob * G
            loss.backward()
        self.optimizer.step()

        self.states, self.actions, self.rewards = [], [], []
