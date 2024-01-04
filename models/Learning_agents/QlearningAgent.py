import torch
import torch.nn as nn
import torch.optim as optim
from State_manager_code.StateManager import  *
import random

from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, experience):
        """Adds an experience to the buffer."""
        self.buffer.append(experience)

    def sample(self, batch_size):
        """Samples a batch of experiences from the buffer."""
        batch_size = min(batch_size, len(self.buffer))
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class QNetwork(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=64):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
class DQN_Agent:
    def __init__(self):
        self.state_manager = StateManager()
        self.state_size = 1
        self.action_size = self.state_manager.get_action_size()
        self.q_network = QNetwork(self.state_size, self.action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)

        # Other parameters
        self.epsilon = 0.1
        self.discount_factor = 0.9
        self.replay_buffer = ReplayBuffer(capacity=10000)

    def choose_action(self, state):
        print("states",state)
        state = torch.from_numpy(state).float().unsqueeze(0)
        if random.random() < self.epsilon:
            action = random.randrange(self.action_size)
        else:
            q_values = self.q_network(state).detach()
            action = torch.argmax(q_values).item()
        return action
    def remember(self, state, action, reward, next_state):
        """Stores experience in the replay buffer."""
        self.replay_buffer.add((state, action, reward, next_state))

    def should_update(self, batch_size=32):
        """Check if the buffer has enough experiences to sample a batch."""
        return len(self.replay_buffer) >= batch_size

    def learn(self, batch_size):
        if len(self.replay_buffer) < batch_size:
            return  # Not enough samples to train

        minibatch = self.replay_buffer.sample(batch_size)
        for state, action, reward, next_state in minibatch:
            state = torch.tensor(state, dtype=torch.float32)
            next_state = torch.tensor(next_state, dtype=torch.float32)
            action = torch.tensor([action], dtype=torch.int64)
            reward = torch.tensor([reward], dtype=torch.float32)

            q_values = self.q_network(state)
            next_q_values = self.q_network(next_state).detach()
            q_value = q_values.gather(1, action.unsqueeze(-1)).squeeze(-1)
            max_next_q_value = next_q_values.max(1)[0]
            expected_q_value = reward + self.discount_factor * max_next_q_value

            loss = nn.MSELoss()(q_value, expected_q_value)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()