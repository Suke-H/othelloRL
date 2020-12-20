import sys
import random
import numpy as np

# from check import check

from collections import deque
import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")

k = 192
fcl_units = 256

# モデル定義
class DQNNet(torch.nn.Module):

    def __init__(self):
        super(DQNNet, self).__init__()
        self.conv1 = nn.Conv2d(2, k, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(k)
        self.conv2 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(k)
        self.conv3 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(k)
        self.conv4 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(k)
        self.conv5 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(k)
        self.conv6 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm2d(k)
        self.conv7 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm2d(k)
        self.conv8 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn8 = nn.BatchNorm2d(k)
        self.conv9 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn9 = nn.BatchNorm2d(k)
        self.conv10 = nn.Conv2d(k, k, kernel_size=3, padding=1)
        self.bn10 = nn.BatchNorm2d(k)
        self.fcl1 = nn.Linear(k * 64, fcl_units)
        self.fcl2 = nn.Linear(fcl_units, 64)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = F.relu(self.bn5(self.conv5(x)))
        x = F.relu(self.bn6(self.conv6(x)))
        x = F.relu(self.bn7(self.conv7(x)))
        x = F.relu(self.bn8(self.conv8(x)))
        x = F.relu(self.bn9(self.conv9(x)))
        x = F.relu(self.bn10(self.conv10(x)))
        x = F.relu(self.fcl1(x.view(-1, k * 64)))
        x = self.fcl2(x)
        return x.tanh()

def train_model(model, x, y, optimizer, criterion):
    # model.train()
    #scheduler.step()
 
    # stateをCNN用に変換
    x = state_transform(x)

    x = torch.from_numpy(x)
    y = torch.from_numpy(y)
    x, y = x.to(device), y.to(device)
 
    optimizer.zero_grad()
    outputs = model(x)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

    return loss

def state_transform(state):
    """
    状態（ボード）をCNNの入力用に変換
    
    入力
    ・(N,8,8)
    ・0が空、1がplayer1の石、2がplayer2の石

    出力
    ・(N,2,8,8)
    ・player1と2の石(1)を2チャンネルで構成
    """

    if len(state.shape) == 2:
        tmp_state = np.copy(state)
        tmp_state = tmp_state.reshape(1, 8, 8)

    else:
        tmp_state = np.copy(state)

    state_1 = np.where(tmp_state==1, 1, 0)
    state_2 = np.where(tmp_state==2, 1, 0)
    tmp_state = np.array([state_1, state_2], dtype=np.float32)
    tmp_state = tmp_state.transpose(1, 0, 2, 3)

    return tmp_state

# # ランダムに石を置くだけのAI
# def randomAI(board, stalement):

#     hand = random.choice(stalement)
#     stones, board = check(board, hand[0], hand[1], 2)

#     return hand, board

# ランダムに石を置くだけのAI
class random_agent:

    # def __init__(self, enable_actions):
    #     self.enable_actions = enable_actions
    #     self.n_actions = len(self.enable_actions)

    def select_action(self, state, legal_hands):
        return random.choice(legal_hands)


class DQNAgent:
    """
    Multi Layer Perceptron with Experience Replay
    """

    def __init__(self):
        # parameters
        # self.name = os.path.splitext(os.path.basename(__file__))[0]
        # self.environment_name = environment_name
        # self.enable_actions = enable_actions
        # self.n_actions = len(self.enable_actions)
        self.minibatch_size = 256
        self.replay_memory_size = 131072
        self.discount_factor = 0.99
        self.epsilon = 0.1
        # self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        # self.model_name = "{}.ckpt".format(self.environment_name)
        
        # replay memory
        self.D = deque(maxlen=self.replay_memory_size)

        # model
        # self.init_model()
        self.model = DQNNet().to(device)

        self.criterion = nn.MSELoss()
        # self.criterion = nn.CrossEntropyLoss()
        # self.optimizer = optim.SGD(self.model.parameters(), lr=10**(-4))
        self.optimizer = optim.RMSprop(self.model.parameters(), lr=10**(-5))
        # self.optimizer = optim.Adam(self.model.parameters(), lr=10**(-2))

        # ログ用
        self.current_loss = 0.0

    def Q_values(self, state):
        """
        stateを入力にして各actionのQ(0~63の行動価値)を出力

        """
        # stateをCNN用に変換
        x = state_transform(state)

        x = torch.from_numpy(x)
        x = x.to(device)
        outputs = self.model(x)

        # 出力は(1,64)なので(64,)にする
        return outputs.data.cpu().numpy()[0]

    def select_action(self, state, legal_hands):
        """
        epsilon-greedyによりstateから次のactionを出力

        """
        if np.random.rand() <= self.epsilon:
            # ランダム
            return np.random.choice(legal_hands)
        else:
            # DQNによる行動選択
            output = self.Q_values(state)
            
            # 合法手から最大の戦略をとる
            non_legal_hands = np.delete(np.array([i for i in range(64)]), np.array(legal_hands))
            output[non_legal_hands] = -np.inf
            return np.argmax(output)

    def store_experience(self, state, action, reward, state_1, terminal):
        # self.D.append((state_transform(state), action, reward, state_transform(state_1), terminal))
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
        # state_minibatch = state_minibatch.reshape(state_minibatch.shape[0], 64)

        self.current_loss = train_model(self.model, state_minibatch, y_minibatch, self.optimizer, self.criterion)

