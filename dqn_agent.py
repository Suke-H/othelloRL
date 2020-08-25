from collections import deque
import os
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# モデル定義
class DQNNet(torch.nn.Module):
    def __init__(self):
        super(DQNNet, self).__init__()
        self.fc1 = torch.nn.Linear(64, 64)
        self.fc2 = torch.nn.Linear(64, 3)
 
    def forward(self, x):
        # テンソルのリサイズ: (N, 1, 2, 1) --> (N, 2)
        # x = x.view(-1, 2)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        # 出力関数
        # return F.softmax(x, dim=0)
        return x

def train_model(model, x, y, optimizer, criterion):
    # model.train()
    #scheduler.step()
 
    # images, labels = images.to(device), labels.to(device)

    x = torch.from_numpy(x)
    y = torch.from_numpy(y)
 
    optimizer.zero_grad()
    outputs = model(x)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

    return loss

class DQNAgent:
    """
    Multi Layer Perceptron with Experience Replay
    """

    def __init__(self, enable_actions, environment_name):
        # parameters
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.environment_name = environment_name
        self.enable_actions = enable_actions
        self.n_actions = len(self.enable_actions)
        self.minibatch_size = 32
        self.replay_memory_size = 1000
        self.learning_rate = 0.001
        self.discount_factor = 0.9
        self.exploration = 0.1
        self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        self.model_name = "{}.ckpt".format(self.environment_name)
        
        # replay memory
        self.D = deque(maxlen=self.replay_memory_size)

        # model
        # self.init_model()
        self.model = DQNNet()

        self.criterion = nn.MSELoss()
        # self.optimizer = optim.SGD(self.model.parameters(), lr=10**(-4))
        self.optimizer = optim.RMSprop(self.model.parameters(), lr=10**(-3))

        # ログ用
        self.current_loss = 0.0

    def Q_values(self, state):
        """
        stateを入力にして各actionのQ(0,1,2の行動価値)を出力

        stateは1つだけなので、
        ・stateを(1, 64)にしてmodelに入力する
        ・出力は(1,3)なので(3,)にする

        """
        # stateを(1, 64)にしてmodelに入力する
        state = state.reshape(1, 64).astype(np.float32)
        x = torch.from_numpy(state)

        outputs = self.model(x)

        # 出力は(1,3)なので(3,)にする
        return outputs.data.cpu().numpy()[0]

    def select_action(self, state, epsilon):
        """
        epsilon-greedyによりstateから次のactionを出力

        stateは1つだけなので、
        ・stateを(1, 64)にしてmodelに入力する
        ・出力は(1,3)なので(3,)にする

        """
        if np.random.rand() <= epsilon:
            # ランダム
            return np.random.choice(self.enable_actions)
        else:
            # DQNによる行動選択
            output = self.Q_values(state.flatten())
            return np.argmax(output)

    def store_experience(self, state, action, reward, state_1, terminal):
        self.D.append((state, action, reward, state_1, terminal))

    def experience_replay(self):
        state_minibatch = []
        y_minibatch = []

        # ミニバッチサイズ(Dがミニバッチサイズ分たまってなかったらDの長さ)
        minibatch_size = min(len(self.D), self.minibatch_size)
        # Dからミニバッチをランダムに選んで作成
        minibatch_indexes = np.random.randint(0, len(self.D), minibatch_size)

        for j in minibatch_indexes:
            state_j, action_j, reward_j, state_j_1, terminal = self.D[j]

            y_j = self.Q_values(state_j)

            if terminal:
                y_j[action_j] = reward_j
            else:
                # reward_j + gamma * max_action' Q(state', action')
                y_j[action_j] = reward_j + self.discount_factor * np.max(self.Q_values(state_j_1))

            state_minibatch.append(state_j)
            y_minibatch.append(y_j)

        # 学習
        state_minibatch, y_minibatch = np.array(state_minibatch).astype(np.float32), np.array(y_minibatch)
        state_minibatch = state_minibatch.reshape(state_minibatch.shape[0], 64)

        self.current_loss = train_model(self.model, state_minibatch, y_minibatch, self.optimizer, self.criterion)

