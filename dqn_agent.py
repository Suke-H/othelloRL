from collections import deque
import os
import numpy as np
from tqdm import tqdm

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
        return F.softmax(x, dim=0)

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
 
    # _, predicted = torch.max(outputs.data, 1)
    # print(predicted)
    # print(y)
    # correct = (predicted == y).sum().item()
 
    # print("Train Acc : %.4f" % (correct/len(y)))

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
        self.optimizer = optim.SGD(self.model.parameters(), lr=10**(-4))

        # variables
        # self.current_loss = 0.0

    # def init_model(self):
    #     # input layer (8 x 8)
    #     self.x = tf.placeholder(tf.float32, [None, 8, 8])

    #     # flatten (64)
    #     x_flat = tf.reshape(self.x, [-1, 64])

    #     # fully connected layer (32)
    #     W_fc1 = tf.Variable(tf.truncated_normal([64, 64], stddev=0.01))
    #     b_fc1 = tf.Variable(tf.zeros([64]))
    #     h_fc1 = tf.nn.relu(tf.matmul(x_flat, W_fc1) + b_fc1)

    #     # output layer (n_actions)
    #     W_out = tf.Variable(tf.truncated_normal([64, self.n_actions], stddev=0.01))
    #     b_out = tf.Variable(tf.zeros([self.n_actions]))
    #     self.y = tf.matmul(h_fc1, W_out) + b_out

    #     # loss function
    #     self.y_ = tf.placeholder(tf.float32, [None, self.n_actions])
    #     self.loss = tf.reduce_mean(tf.square(self.y_ - self.y))

    #     # train operation
    #     optimizer = tf.train.RMSPropOptimizer(self.learning_rate)
    #     self.training = optimizer.minimize(self.loss)

    #     # saver
    #     self.saver = tf.train.Saver()

    #     # session
    #     self.sess = tf.Session()
    #     self.sess.run(tf.global_variables_initializer())

    def Q_values(self, state):
        # Q(state, action) of all actions
        # stateは一つ、バッチではない
        state = state.reshape(1, 64).astype(np.float32)
        x = torch.from_numpy(state)
        outputs = self.model(x)
        # _, predicted = torch.max(outputs.data, 1)
        print(outputs)
        print(outputs.data.cpu().numpy()[0])

        # return predicted.item()
        return outputs.data.cpu().numpy()[0]

    def select_action(self, state, epsilon):
        # stateは一つ、バッチではない
        if np.random.rand() <= epsilon:
            # random
            return np.random.choice(self.enable_actions)
        else:
            # max_action Q(state, action)

            # # stateを(1, 64)にする
            # x = state[np.newaxis, :, :]
            # x = x.reshape(1, 64)
            output = self.Q_values(state.flatten())
            return np.argmax(output)

    def store_experience(self, state, action, reward, state_1, terminal):
        self.D.append((state, action, reward, state_1, terminal))

    def experience_replay(self):
        state_minibatch = []
        y_minibatch = []

        # sample random minibatch
        minibatch_size = min(len(self.D), self.minibatch_size)
        minibatch_indexes = np.random.randint(0, len(self.D), minibatch_size)

        for j in minibatch_indexes:
            state_j, action_j, reward_j, state_j_1, terminal = self.D[j]
            # action_j_index = self.enable_actions.index(action_j)
            action_j_index = action_j

            y_j = self.Q_values(state_j)

            if terminal:
                y_j[action_j_index] = reward_j
            else:
                # reward_j + gamma * max_action' Q(state', action')
                y_j[action_j_index] = reward_j + self.discount_factor * np.max(self.Q_values(state_j_1))

            state_minibatch.append(state_j)
            y_minibatch.append(y_j)

        # training

        state_minibatch, y_minibatch = np.array(state_minibatch).astype(np.float32), np.array(y_minibatch)
        state_minibatch = state_minibatch.reshape(state_minibatch.shape[0], 64)
        print(state_minibatch.shape, y_minibatch.shape)

        train_model(self.model, state_minibatch, y_minibatch, self.optimizer, self.criterion)

        # for log
        # self.current_loss = self.sess.run(self.loss, feed_dict={self.x: state_minibatch, self.y_: y_minibatch})

    # def load_model(self, model_path=None):
    #     if model_path:
    #         # load from model_path
    #         self.saver.restore(self.sess, model_path)
    #     else:
    #         # load from checkpoint
    #         checkpoint = tf.train.get_checkpoint_state(self.model_dir)
    #         if checkpoint and checkpoint.model_checkpoint_path:
    #             self.saver.restore(self.sess, checkpoint.model_checkpoint_path)

    # def save_model(self):
    #     self.saver.save(self.sess, os.path.join(self.model_dir, self.model_name))
