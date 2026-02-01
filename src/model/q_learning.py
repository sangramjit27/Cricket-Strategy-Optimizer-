
import numpy as np

class BattingRL:
    def __init__(self, num_states=100, num_actions=3):
        self.Q = np.zeros((num_states, num_actions))
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.Q.shape[1])  # Explore
        else:
            return np.argmax(self.Q[state])  # Exploit

    def update(self, state, action, reward, next_state):
        self.Q[state, action] = (1 - self.alpha) * self.Q[state, action] + self.alpha * (
            reward + self.gamma * np.max(self.Q[next_state])
        )

    def recommend(self, state):
        action = np.argmax(self.Q[state])
        return ['Attack', 'Defend', 'Rotate'][action]
